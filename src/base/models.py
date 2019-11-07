# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

import datetime
import time
import random
from hashlib import sha512
from player.Logger import Logger

# Create your models here.

USER_TYPE_WEB = 1
USER_TYPE_SKYPE = 2
USER_TYPES = (
	(USER_TYPE_WEB, 'Web'),
	(USER_TYPE_SKYPE, 'Skype'),
)

class User(models.Model):
	id = models.AutoField(primary_key = True)
	active = models.BooleanField(default = False)
	type = models.IntegerField(choices = USER_TYPES)
	login = models.TextField(unique = True)
	password = models.TextField(default = "", blank=True)
	salt = models.TextField(default = time.time)
	
	displayName = models.TextField(unique = True)
	
	def __str__(self):
		return self.login
	
	def PasswordHash(self, password):
		if self.salt is None or len(str(self.salt)) < 1:
			raise "Salt not found..."
		
		passwordSalted = password + str(self.salt)
		return sha512(passwordSalted.encode('ascii')).hexdigest()

class Song(models.Model):
	id = models.AutoField(primary_key = True)
	active = models.BooleanField(default = True)
	url = models.TextField()
	title = models.TextField()
	date = models.DateTimeField(auto_now = True)
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	
	queueCounter = models.IntegerField(default = 0)
	skipCounter = models.IntegerField(default = 0)
	
	def __str__(self):
		return self.title

class ShuffleItem(models.Model):
	id = models.AutoField(primary_key = True)
	song = models.ForeignKey(Song, on_delete=models.DO_NOTHING)

class QueueItem(models.Model):
	id = models.AutoField(primary_key = True)
	song = models.ForeignKey(Song, on_delete=models.DO_NOTHING)
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	
class AuthToken(models.Model):
	token = models.TextField(primary_key = True)
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	address = models.GenericIPAddressField()
	lastUsed = models.DateTimeField(auto_now = True)
	
	@staticmethod
	def Generate(userType, address, login, password = ""):
		userType = int(userType)
		
		if userType != USER_TYPE_WEB and userType != USER_TYPE_SKYPE:
		#if userType not in USER_TYPES:
			print("Invalid user type!")
			return None
		
		if userType == USER_TYPE_SKYPE and address != "127.0.0.1":
			print("Wrong address? {} , {}".format(userType != USER_TYPE_SKYPE, address != "127.0.0.1"))
			return None
		
		try:
			user = User.objects.get(login = login)
			if user is None or user.active == False or userType != user.type:
				Logger.instance().Log("Account \"{}\" is disabled, contact your administrator!".format(login))
				print("Account inactive? {} ?= {}".format(userType, user.type))
				print("{}, {}, {}".format(user is None, user.active == False, userType != user.type))
				return None
		except:
			print("No user - " + login)
			return None
		
		if user.type == USER_TYPE_WEB:
			passwordHash = user.PasswordHash(password) #str(sha512(password + user.salt))
			if passwordHash != user.password:
				print("Wrong password hash")
				return None
			
		print("Removing old tokens!")
		#AuthToken.delete(user = user)
		oldTokens = AuthToken.objects.filter(user = user)
		for ot in oldTokens:
			print("Deleting token: {}".format(ot.token))
			ot.delete()
			
		print("Generating new token!")
		token = AuthToken()
		#print "Token = {} {} {}".format(str(sha512(str(time.time()))), login, str(random.random()))
		tokenRandomValue = str(time.time()) + login + str(random.random())
		token.token = sha512(tokenRandomValue.encode('ascii')).hexdigest()
		token.user = user
		token.address = address
		token.save()
		
		return token
	
	@staticmethod
	def Delete(token_str):
		try:
			token = AuthToken.objects.get(token = token_str)
			token.delete()
		except:
			pass
		
	@staticmethod
	def Get(token_str):
		try:
			return AuthToken.objects.get(token = token_str)
		except:
			return None
	
	@staticmethod
	def Validate(token_str):
		try:
			token = AuthToken.objects.get(token = token_str)
		except:
			return False
		
		if token.isValid():
			token.lastUsed = datetime.datetime.now()
			token.save()
			return True
		else:
			token.delete()
			return False 
	
	def isValid(self):
		if self.user.active is False:
			return False
		
		if (datetime.datetime.now() - self.lastUsed.replace(tzinfo=None)).total_seconds() > 8*60*60:
			return False
		
		return True
	