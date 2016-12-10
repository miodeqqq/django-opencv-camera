# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify
import os

def upload_images_path(instance, filename):
    """
    Upload path for images files in Image model.
    """

    file_name, ext = os.path.splitext(filename)

    return os.path.join(u'images/{file_name}{ext}'.format(
        file_name=slugify(file_name),
        ext=ext
    ))

class Image(models.Model):
    """
    Image model - to be uploaded in Django-Admin.
    """

    title = models.CharField('Image title', max_length=255)
    image = models.ImageField('Image file', upload_to=upload_images_path, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
