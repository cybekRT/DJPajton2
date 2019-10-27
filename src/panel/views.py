# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views import View

from player.Player import Player
from base.models import AuthToken, User, USER_TYPE_SKYPE, USER_TYPE_WEB

# Create your views here.
def Index(request):
	player = Player.instance()
	model = {}
	model["song"] = player.getCurrentSong()
	model["time"] = player.getTime()
	model["length"] = player.getLength()
	model["volume"] = player.getVolume()
	
	return HttpResponse(render(request, 'index.html', context = model))

#def Login(request):
#	if request.method == "POST"
#	#return HttpResponse("Login panel :)")

class Register(View):
	def get(self, request):
		return HttpResponse(render(request, "register.html"))
	
	def post(self, request):
		
		data = request.POST
		
		type = int(data['type'])
		login = data['login']
		password = data['password']
		password2 = data['password2']
		displayName = data['displayName']
		address = request.META['REMOTE_ADDR']
		
		user = User()
		user.type = type
		user.login = login
		if type == USER_TYPE_WEB:
			if password != password2:
				raise "Wrong password"
			#user.password = password
			user.password = user.PasswordHash(password)
		
		if type == USER_TYPE_SKYPE and address != "127.0.0.1":
			print "Hack attempt!!!"
			return redirect('/register?error=1&please_stop_hacking_this_site=667')
		
		user.displayName = displayName
		
		try:
			user.save()
		except Exception as e:
			return HttpResponse("Registration failed: {}".format(e), status = 401)
		
		msg = "<pre>OK, now wait for activation of your account...\n\nUser id: {}</pre>".format(user.id)
		return HttpResponse(msg)

class Login(View):
	def get(self, request):
		return HttpResponse(render(request, "login.html"))
	
	def post(self, request):
		
		data = request.POST
		
		type = int(data['type'])
		if type != USER_TYPE_WEB:
			print "Hack attempt!!!"
			return redirect('/login?error=1&please_stop_hacking_this_site=666')
		
		login = data['login']
		password = data['password']
		address = request.META['REMOTE_ADDR']
		
		print "Address: {}".format(address)
		
		token = AuthToken.Generate(USER_TYPE_WEB, address, login, password)
		if token is None:
			return redirect('/login?error=1')
		print("Token: " + str(token))
		
		#response = HttpResponse("POST xd: <pre>" + str(request.COOKIES) + "\n\nGET: " + str(request.GET.lists()) + "\n\nPOST: " + str(request.POST.lists()) + "\n\n" + str(dir(request)) + "\n\nToken: " + token.token + "</pre>")
		response = redirect('/') 
		
		#response.cookies['token'] = token.token
		response.set_cookie('token', token.token)
		
		print request.POST
		return response
	
class Logout(View):
	def get(self, request):
		response = redirect('/')
		
		if 'token' in request.COOKIES:
			AuthToken.Delete(request.COOKIES['token'])
		
		response.set_cookie('token', expires=0)
		return response
	
class Token(View):
	def get(self, request, userId):
		print str(request)
		print str(request.META)
		token = AuthToken.Generate(USER_TYPE_SKYPE, request.META['REMOTE_ADDR'], userId)
		if token is None:
			return HttpResponse("Invalid request", status = 400)
		
		return HttpResponse(token.token)
	