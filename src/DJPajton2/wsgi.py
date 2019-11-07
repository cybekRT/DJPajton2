"""
WSGI config for DJPajton2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from player.Player import Player
from skype.Skype import Skype

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DJPajton2.settings")

# Start player
vlc = Player.instance()

try:
	skype = Skype.instance()
	skype.start()
except:
	print("Skype initialization failed! Use web panel :(")

print("Started!")
application = get_wsgi_application()
