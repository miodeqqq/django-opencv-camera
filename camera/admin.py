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
        'get_input_image_url',
        'get_processed_image_url',
        'processing_output_info',
        'date_created'
    ]

    exclude = ['output_image',]

    readonly_fields = ['processing_output_info',]

    def get_input_image_url(self, obj):
        if obj.input_image:
            return format_html(u'<a href="{img_path}" target="_blank">{img_name}</a>'.format(
                img_path=obj.input_image.url,
                img_name=truncatechars(os.path.basename(obj.input_image.path), 35)
            ))

    get_input_image_url.allow_tags = True
    get_input_image_url.short_description = 'Input Image'

    def get_processed_image_url(self, obj):
        if obj.output_image:
            return format_html(u'<a href="{img_path}" target="_blank">{img_name}</a>'.format(
                img_path=obj.output_image.url,
                img_name=truncatechars(os.path.basename(obj.output_image.path), 35)
            ))

    get_processed_image_url.allow_tags = True
    get_processed_image_url.short_description = 'Output Image'
