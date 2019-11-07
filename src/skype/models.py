# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class SkypeConfig(models.Model):
	active = models.BooleanField(default = True)
	login = models.TextField()
	password = models.TextField()
	groupAddress = models.TextField()
