# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.urls import path, include
from django.contrib import admin
from example.apps.main import urls as main_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(main_urls)),
]
