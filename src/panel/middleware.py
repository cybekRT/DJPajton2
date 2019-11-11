from django.shortcuts import redirect
from django.http.response import HttpResponse
from base.models import AuthToken
from player.Logger import Logger

class CSP:
	def __init__(self, get_response):
		self.get_response = get_response
		
	def __call__(self, request):
		response = self.get_response(request)
		#response["Content-Security-Policy"] = "default-src * 'unsafe-inline' 'unsafe-eval'; script-src * 'unsafe-inline' 'unsafe-eval'; connect-src * 'unsafe-inline'; img-src * data: blob: 'unsafe-inline'; frame-src *; style-src * 'unsafe-inline';"
		response["Content-Security-Policy"] = "default-src *  data: blob: 'unsafe-inline' 'unsafe-eval'; script-src * data: blob: 'unsafe-inline' 'unsafe-eval'; connect-src * data: blob: 'unsafe-inline'; img-src * data: blob: 'unsafe-inline'; frame-src * data: blob: ; style-src * data: blob: 'unsafe-inline';font-src * data: blob: 'unsafe-inline';"
		return response
	
class PanelAuth:
	def __init__(self, get_response):
		self.get_response = get_response
		
	def __call__(self, request):
		if request.path.startswith("/login") or request.path.startswith("/register") or request.path.startswith("/admin/") or request.path.startswith("/token") or request.path.startswith('/api/logger'):
			response = self.get_response(request)
		elif self.validateToken(request):
			token_str = request.COOKIES['token']
			token = AuthToken.Get(token_str)
			pathsToIgnore = [
				"/",
				"/api/status",
				"/api/queue",
				"/api/playlist",
				"/api/playlist/all",
				"/api/users",
			]
			#if request.path != "/api/status" and request.path != "/api/queue":
			if request.path not in pathsToIgnore:
				Logger.instance().Log("{} -> {}".format(token.user.displayName, request.path))
			response = self.get_response(request)
		elif request.path.startswith("/api"):
			response = HttpResponse("Access denied!", status = 401)
			response.delete_cookie('token')
		else:
			response = redirect('/login')
			response.delete_cookie('token')
			
		return response
	
	def validateToken(self, request):
		if 'token' not in request.COOKIES:
			print("No token in cookies :(")
			return False
		
		token_str = request.COOKIES['token']
		token = AuthToken.Get(token_str)
		
		if token is None:
			return False
		
		print("{} - {}".format(token.user.displayName, request.path))
		
		return token.isValid()
		#return AuthToken.Validate(token)
	