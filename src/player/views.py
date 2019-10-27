# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from player.Player import Player
from django.http.response import HttpResponse
from base.models import Song
from django.core import serializers
from player.Logger import Logger
import json
from time import sleep

# Create your views here.
def GetVolume(request):
	return HttpResponse(Player.instance().getVolume())

def SetVolume(request, volume):
	volume = int(volume)
	Player.instance().setVolume(volume)
	return HttpResponse(Player.instance().getVolume())

def GetTime(request):
	return HttpResponse(Player.instance().getTime())
	#return "{}".format(Player.instance().getTime())
	
def SetTime(request, time):
	time = int(time)
	Player.instance().setTime(time)
	return HttpResponse(Player.instance().getTime())

def GetLength(request):
	return HttpResponse(Player.instance().getLength())
	
def Start(request):
	Player.instance().start()
	return HttpResponse()
	
def Stop(request):
	Player.instance().stop()
	return HttpResponse()
	
def Next(request):
	Player.instance().nextSong()
	return HttpResponse()

def Playlist(request):
	#blob = json.dumps(list(Song.objects.all()))
	blob = serializers.serialize("json", Song.objects.all())
	return HttpResponse(blob)

def Queue(request, *args):
	print "Queue here: {}".format(args)
	return HttpResponse(str(args))

def Invalid(request):
	print request.path[5:]
	x = request.path[5:].split('/')
	print x
	
	functionName = x[0].lower().capitalize()
	functionParams = x[1:]
	
	import sys
	q = getattr(sys.modules[__name__], functionName)
	try:
		return q(*functionParams)
	except:
		return HttpResponse("Not implemented: {}".format(functionName), status = 501)
	
def LoggerRecent(request):
	recent = Logger.instance().Latest()
	return HttpResponse(recent)

def LoggerSince(request, index):
	index = int(index)
	
	logger = Logger.instance()
	data = logger.GetSince(index)
	return HttpResponse(json.dumps(data))

def LoggerWait(request, index):
	index = int(index)
	
	logger = Logger.instance()
	while index == logger.Latest():
		sleep(1)
		
	return HttpResponse(logger.Latest())
