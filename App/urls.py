#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-27 22:12:34
# @Author  : Root (root@mylonly.com)
# @Version : 1.0.0
# @Description: 


from django.urls import path
from App.views import AppList,CreateApp

urlpatterns = [
    path('list/',AppList.as_view()),
    path('create/',CreateApp.as_view())
]