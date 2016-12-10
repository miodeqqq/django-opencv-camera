# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from .utils import detect_faces_on_image, detect_eyes_on_image

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

    TYPE_CHOICES = (
        (0, 'Face recognition'),
        (1, 'Eyes recognition'),
    )

    title = models.CharField('Image title', max_length=255)
    image = models.ImageField('Image file', upload_to=upload_images_path, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    type = models.BooleanField('Type of processing', help_text='Choose a proper algorithm.', choices=TYPE_CHOICES, default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


@receiver(post_save, sender=Image, dispatch_uid='detect_faces')
def detect_faces(sender, instance, **kwargs):
    if kwargs.get('created', False):
        if instance.type == 0:
            detect_faces_on_image(instance)
        else:
            detect_eyes_on_image(instance)
        instance.save()
