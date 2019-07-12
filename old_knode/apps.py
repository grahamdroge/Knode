# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.contrib.auth.models import User
from actstream import registry



# class VibesiteConfig(AppConfig):
#     name = 'vibesite'


class MyAppConfig(AppConfig):
    name = 'vibesite'
    def ready(self):
        registry.register(User,self.get_model('Interests'),self.get_model('Tools'),self.get_model('Posts'),self.get_model('UserProfile'),self.get_model('SubSections'))
