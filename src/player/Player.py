import os
import vlc
import pafy
import threading
from base.models import Song, ShuffleItem, User, USER_TYPE_SKYPE
from random import shuffle
from __builtin__ import True
from player.Logger import Logger
import json

_player = None

class VLCEventNext(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		Player.instance().nextSong(True)

class Player():
	@staticmethod
	def instance():
		global _player
		if _player is None:
			_player = Player()

		return _player
		
	# VLC
	vlcInstance = None
	vlcPlayer = None
	vlcEvents = None

	currentSong = None
	
	def __init__(self):
		global _player
		if _player is not None:
			raise "Player was initialized!"
		
		print "Starting player..."
		self.vlcInstance = vlc.Instance("--live-caching=0 --network-caching=0 --norm-buff-size=8")
		self.vlcPlayer = self.vlcInstance.media_player_new()
		self.vlcEvents = self.vlcPlayer.event_manager()
		self.vlcEvents.event_attach(vlc.EventType.MediaPlayerEndReached, self.songFinished)
		self.vlcEvents.event_attach(vlc.EventType.MediaPlayerEncounteredError, self.songCorrupted)
		self.vlcEvents.event_attach(vlc.EventType.MediaStateChanged, self.mediaStateChanged)
		
		# Import old DJPajton playlist
		if Song.objects.count() == 0 and os.path.isfile('music4you.playlist'):
			with open("music4you.playlist", "r") as f:
				playlist = json.loads(f.read())
				for item in playlist:
					print "Item: {}".format(item)
					
					song = Song()
					song.id = int(item['id'])
					song.date = item['addedDate']
					song.active = (bool(item['deleted']) == False)
					song.url = item['url']
					song.title = item['title']
					
					try:
						user = User.objects.get(login = item['addedLogin'])
					except:
						user = User()
						user.active = False
						user.type = USER_TYPE_SKYPE
						user.login = item['addedLogin']
						user.displayName = user.login
						user.save()
						
					song.user = user
					song.save() 
		
		#self.vlcPlayer.audio_set_volume(100)
		
		if Song.objects.count() == 0:
			return
		
		#self.nextSong()
		
	# Events
		
	def songFinished(self, event):
		print "Song finished!"
		VLCEventNext().start()
		
	def songCorrupted(self, event):
		print "Song corrupted!"
		self.songFinished(event)
		
	def mediaStateChanged(self, event):
		print "Player state changed!"
		
	def logCurrentQueue(self):
		msg = "DJPajton zapuszcza: {}".format(self.currentSong.title.encode('utf-8'))
		
		Logger.instance().Log(msg)
		return
		
	# Getters / Setters
	
	def shufflePlaylist(self):
		songs = list(Song.objects.filter(active = True).values_list('id', flat = True))
		shuffle(songs)
		print songs
		for a in songs:
			item = ShuffleItem()
			item.song_id = a
			item.save()
			
		Logger.instance().Log("Everyday im shufflin~")
		
	def nextSong(self, force = False):
		if ShuffleItem.objects.count() == 0:
			self.shufflePlaylist()
			
		if ShuffleItem.objects.count() == 0:
			Logger.instance().Log("No songs, add something guys...")
			return
			
		shuffleItem = ShuffleItem.objects.first()
		song = shuffleItem.song
		shuffleItem.delete()
		#song = Song.objects.get(id = 1)
		
		url = pafy.new(song.url).getbestaudio().url
		print "Url: " + url
		self.vlcPlayer.set_mrl(url)
		self.vlcPlayer.play()
		print "Ok!"
		
		self.currentSong = song
		self.logCurrentQueue()
		
	def isPlaying(self):
		return self.vlcPlayer.is_playing() == 1
		
	def start(self):
		if self.isPlaying() is False:
			Logger.instance().Log("Started party!")
			if self.currentSong is None:
				self.nextSong()
			else:
				self.vlcPlayer.play()
				self.logCurrentQueue()
				
			return True
		return False
		
	def stop(self):
		if self.isPlaying():
			self.vlcPlayer.stop()
			Logger.instance().Log("Booooh...")
			return True
		return False
		
	def getCurrentSong(self):
		return self.currentSong
	
	def getTime(self):
		return self.vlcPlayer.get_time() / 1000
	
	def setTime(self, time):
		time = int(time)
		print "Setting time: {} / {}".format(time, self.getLength())
		if time >= 0 and time < self.getLength():
			self.vlcPlayer.set_time(time * 1000)
		return self.getTime()
	
	def getLength(self):
		return self.vlcPlayer.get_length() / 1000
		
	def getVolume(self):
		volume = self.vlcPlayer.audio_get_volume()
		#Logger.instance().Log("Current volume: {}".format(volume))
		return volume
	
	def setVolume(self, volume):
		volume = int(volume)
		
		if volume < 20:
			volume = 20
		if volume > 150:
			volume = 150
		
		self.vlcPlayer.audio_set_volume(volume)
		volume = self.getVolume()
		Logger.instance().Log("Current volume: {}".format(volume))
		return volume