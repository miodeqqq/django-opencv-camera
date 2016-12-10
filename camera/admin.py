# -*- coding: utf-8 -*-


import os

from django.contrib import admin
from django.utils.html import format_html
from .models import Image
from django.template.defaultfilters import truncatechars


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
        image_url = obj.image

        if image_url:
            return format_html(u'<a href="{img_path}" target="_blank">{img_name}</a>'.format(
                img_path=image_url.url,
                img_name=truncatechars(os.path.basename(image_url.path), 35)
            ))

        return '<span style="color:red">PDF input exists!</span>' if obj.pdf_input else '<span style="color:red">Not supported parser yet!</span>'

    get_processed_image_url.allow_tags = True
    get_processed_image_url.short_description = 'Image URL'