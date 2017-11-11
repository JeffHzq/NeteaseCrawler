# -*- coding: utf-8 -*-
from django.db import models

class MusicLanguage(models.Model):
    name = models.CharField(max_length=50)

class Singer(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=1024, null=True, blank=True)
    language = models.ForeignKey(MusicLanguage, verbose_name=u'语种')

class Album(models.Model):
    name = models.CharField(max_length=255)
    time = models.DateField(null=True, blank=True)
    image = models.CharField(max_length=1024, null=True, blank=True)
    describe = models.TextField(null=True, blank=True)
    singer = models.ForeignKey(Singer, verbose_name=u'歌手')

class Music(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=1024)
    duration = models.CharField(max_length=50, null=True, blank=True)
    album = models.ForeignKey(Album, verbose_name=u'专辑', null=True, blank=True)
    singer = models.ForeignKey(Singer, verbose_name=u'歌手', null=True, blank=True)

