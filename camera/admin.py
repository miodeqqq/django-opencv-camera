# -*- coding: utf-8 -*-


import os

from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django.utils.html import format_html

from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Admin for Image model.
    """

    list_display = [
        'title',
        'get_processed_image_url',
        'date_created'
    ]

    def get_processed_image_url(self, obj):
        if obj.image:
            return format_html(u'<a href="{img_path}" target="_blank">{img_name}</a>'.format(
                img_path=obj.image.url,
                img_name=truncatechars(os.path.basename(obj.image.path), 35)
            ))

    get_processed_image_url.allow_tags = True
    get_processed_image_url.short_description = 'Image URL'
