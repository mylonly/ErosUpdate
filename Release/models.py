from django.db import models
from App.models import App
from Package.models import Package
from Device.models import Device
import random

# Create your models here.
class Record(models.Model):
  appName = models.CharField(max_length=100)
  jsVersion = models.CharField(max_length=20, null=True)
  appPlatform = models.CharField(max_length=20)
  appVersion = models.CharField(max_length=20)
  isDiff = models.BooleanField(default=True)
  deviceToken = models.CharField(max_length=100, unique=True)
  deviceName = models.CharField(max_length=50, null=True)
  osVersion = models.CharField(max_length=50, null=True)
  updateJSVersion = models.CharField(max_length=50, null=True)
  updateTime = models.DateTimeField(auto_now=True)
  ip = models.CharField(max_length=100)
  area = models.CharField(max_length=100, null=True)
  


class Release(models.Model):

  FILTER_TYPE = [
    (0, '灰度值'),
    (1, '指定设备'),
  ]

  appName = models.CharField(max_length=100)
  jsVersion = models.CharField(max_length=100)
  android = models.CharField(max_length=100)
  iOS = models.CharField(max_length=100)
  filterType = models.IntegerField(choices=FILTER_TYPE, default=0)
  grayScale = models.FloatField(null=True)  #灰度值
  deviceIDs = models.CharField(max_length=5000, null=True, blank=True)
  createtime = models.DateTimeField(auto_now=True)

  @classmethod
  def gotHit(cls, data):
    appName = data.get('appName')
    appPlatform = data.get('appPlatform')
    appVersion = data.get('appVersion')
    releases = None
    if appPlatform == 'iOS' or appPlatform == 'ios':
      releases = Release.objects.filter(appName=appName, iOS=appVersion).order_by('jsVersion')
    elif appPlatform == 'Android' or appPlatform == 'android':
      releases = Release.objects.filter(appName=appName, android=appVersion).order_by('jsVersion')
    else:
      return None
    for release in releases:
      if release.filterType == 0: #按灰度值来决定是否匹配
        randomGrayscale = random.random()
        if randomGrayscale <= release.grayScale:
          return release.jsVersion
      elif release.filterType == 1: #根据指定设备来匹配
        if release.deviceIDs.find(deviceToken) != -1:
          return release.jsVersion      
      else:
        continue
    return None