import skpy
import os
import re
import sys
import threading
import traceback
import requests
from subprocess import check_output
#from player.Player import Player

from base.models import USER_TYPE_SKYPE
from time import sleep
from models import SkypeConfig

_skype = None

class SkypeLoggerClient(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.recent = -1
		
	def run(self):
		mainEndpoint = Skype.instance().mainEndpoint
		
		while True:
			try:
				waitEndpoint = mainEndpoint + "/api/logger/wait/{}".format(self.recent)
				r = requests.get(waitEndpoint)
				
				current = int(r.text)
				
				getEndpoint = mainEndpoint + "/api/logger/{}".format(self.recent)
				r = requests.get(getEndpoint)
				data = r.json()
				
				for item in data:
					Skype.instance().sendMsg(item)
					
				self.recent = current
			except Exception as e:
				Skype.instance().sendMsg("SkypeLoggerClient exception: {}".format(e))
				sleep(5)
			

class Skype(skpy.SkypeEventLoop, threading.Thread):
	
	commands = (
		("^help$", "Help", "Displays this message..."),
		("^ping$", "Ping", "Pong?"),
		("^register$", "Register", "Registers your account to use this API"),
		("^start$", "Start", "Starts the party~!"),
		("^stop$", "Stop", "Ohh..."),
		("^next$", "Next", "Next song, spam starts again..."),
		("^queue$", "Queue", "Displays current queue"),
		("queue.*?([0-9 ]+)", "Queue", "Adds songs to queue"),
		("^queue$", "Queue", "Prints current queue"),
		("vol.*?([0-9]+)", "Volume", "Changes current volume"),
		("^vol$", "Volume", "Gets current volume"),
	)
	
	tokens = {
		
	}
	
	mainEndpoint = "http://127.0.0.1:8000"
	
	@staticmethod
	def instance():
		global _skype
		if _skype is None:
			_skype = Skype()

		return _skype

	def __init__(self):
		global _skype
		if _skype is not None:
			raise "Skype was initialized!"
			
		try:
			config = SkypeConfig.objects.last()
			if config.active == False:
				raise
		except:
			raise Exception("Missing/Inactive skype configuration...")
		
		print "Logging in to skype..."
		
		if os.path.isfile('.skpy-token') is False:
			open('.skpy-token', 'a').close()
		
		super(Skype, self).__init__(config.login, config.password, ".skpy-token")
		threading.Thread.__init__(self)

		#if os.path.isfile(historyDatePath):
		#	with open(historyDatePath, 'r') as f:
		#		dateStr = json.loads(f.read())
		#		self.lastDate = dateutil.parser.parse(dateStr)
		#print "Last date: {0}".format(self.lastDate)

		groupId = self.chats.urlToIds(config.groupAddress)['id']
		self.chat = self.chats.chat(groupId)
		self.firstRun = True

	def sendMsg(self, msg):
		if msg is None or len(msg) == 0:
			return
		
		#if len(msg) > 1024:
		#	self.sendMsg(msg[:1024])
		#	self.sendMsg(msg[1025:])
		#	return

		try:
			self.chat.sendMsg(msg)
		except Exception as e:
			if len(msg) > 1024:
				self.sendMsg(msg[:1024])
			print "Skajpaj siadl...?"
			print e
			return

	def run(self):
		self.loggerClient = SkypeLoggerClient()
		self.loggerClient.start()
		
		if self.firstRun is True:
			try:
				ip = check_output(['hostname', '--all-ip-addresses']).strip()
			except:
				ip = ""
			#self.sendMsg("DJ Pajton zaprasza na imprezke~!\n\nMoj adres IP: {}\nPanel administracyjny: http://{}:{}/".format(ip, ip, sys.argv[-1]))
			self.sendMsg("DJ Pajton zaprasza na imprezke~!\n\nMoj adres IP: {}\nPanel administracyjny: http://{}/".format(ip, sys.argv[-1]))
			self.firstRun = False

		print "Started skype!"
		self.loop()
		
	def onEvent(self, event):
		try:
			if isinstance(event, skpy.SkypeNewMessageEvent) and event.msg.userId != self.userId and event.msg.chat.id == self.chat.id:
				self.handleEvent(event)
		except Exception as e:
			tb = traceback.format_exc()
			self.sendMsg("Ktos cos popsul:\n\n{}\n\n{}".format(e, tb))
		
	def handleEvent(self, event):
		#print event
		msg = event.msg
		cmd = msg.content.strip().lower()
		userId = msg.userId
		
		for regex in self.commands:
			print "Testing regex: \"{}\" ?= \"{}\"".format(cmd, regex[0])
			m = re.search(regex[0], cmd)
			if m is not None:
				try:
					print "Found handler!!!"
					functionName = regex[1]
					functionParams = m.groups()
					handler = getattr(self, functionName)
					return handler(userId, *functionParams)
				except Exception as e:
					print "Exception: {}".format(e)
					self.sendMsg("Exception: {}".format(e))
					return
				
	def Request(self, userId, *args):
		#args.join('/')
		
		#print userId
		if userId in self.tokens:
			print "Existing token - {}...".format(userId)
			token = self.tokens[userId]
		else:
			print "Generating new token for: {}".format(userId)
			req = requests.get(url = self.mainEndpoint + "/token/{}".format(userId))
			if req.status_code != 200:
				raise Exception("No token for user: {}".format(userId))
				return None
			
			token = req.text
			self.tokens[userId] = token
		
		endpoint = self.mainEndpoint + "/api/" + "/".join(map(str, args))
		print "Endpoint: {}".format(endpoint)
		
		req = requests.get(url = endpoint, cookies = {'token': token})
		print req.text
		return req.text
	
	def getNameByUserId(self, userId):
		try:
			for v in self.chat.users:
				if v.id == userId:
					name = ""
					if v.name.first is not None:
						name = name + v.name.first
					if v.name.last is not None:
						if len(name) > 0:
							name = name + " "
						name = name + v.name.last
					return name
		except:
			return "<Anonymous :( >"
		return "<Anonymous :-( >"
		
	def Help(self, userId):
		msg = "Pomagam!\n"
		for cmd in self.commands:
			msg = msg + "\n{} - {}".format(cmd[0], cmd[2])
			
		self.sendMsg(msg)
		
	def Ping(self, userId):
		self.sendMsg("Pong~")
		
	def Register(self, userId):
		endpoint = self.mainEndpoint + "/register"
		
		s = requests.Session()
		s.get(url = endpoint)
		print "Cookies: {}".format(s.cookies)
		
		data = {
			'type': USER_TYPE_SKYPE,
			'login': userId,
			'password': '',
			'password2': '',
			'displayName': self.getNameByUserId(userId),
			'csrfmiddlewaretoken': s.cookies['csrftoken']
		}
		
		try:
			req = s.post(url = endpoint, data = data)
			#if req.status_code != 200:
			#	result = "Invalid request!"
			#else:
			result = req.text
		except Exception as e:
			result = "exception: {}".format(e)
		self.sendMsg("Register result: {}".format(result))
		
	def Start(self, userId):
		self.Request(userId, "start")
		
	def Stop(self, userId):
		self.Request(userId, "stop")
		
	def Next(self, userId):
		self.Request(userId, "next")

	def Queue(self, userId, ids = None):
		#print len(args)
		print "Ohh"
		if ids is not None:
			self.Request(userId, "queue/{}".format(ids))
		else:
			self.Request(userId, "queue")

	def Volume(self, userId, volume = None):
		
		if volume is not None:
			volume = self.Request(userId, "volume", volume)
		else:
			volume = self.Request(userId, "volume")
			self.sendMsg("Current volume: {}".format(volume))
			
		#self.sendMsg("Current volume: {}".format(volume))

















