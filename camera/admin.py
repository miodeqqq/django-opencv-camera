# -*- coding: utf-8 -*-


import os

from django.contrib import admin

from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Admin for Image model.
    """

    list_display = [
        'title',
        'image'
    ]
