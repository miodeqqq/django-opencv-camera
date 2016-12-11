# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from .utils import detect_faces_on_image, detect_eyes_on_image, detect_barcode_on_image

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
        (2, 'Barcode recognition'),
    )

    title = models.CharField('Image title', max_length=255)
    input_image = models.ImageField('Input image', upload_to=upload_images_path, blank=True, null=True)
    output_image = models.ImageField('Output image', upload_to=upload_images_path, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    type = models.IntegerField('Type of processing', help_text='Choose a proper algorithm.', choices=TYPE_CHOICES, default=0)
    processing_output_info = models.CharField('Processing info output', blank=True, max_length=255)

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


@receiver(post_save, sender=Image, dispatch_uid='algorithms_processing')
def algorithms_processing(sender, instance, **kwargs):
    if kwargs.get('created', False):
        if instance.type == 0:
            detect_faces_on_image(instance)
        elif instance.type == 1:
            detect_eyes_on_image(instance)
        else:
            detect_barcode_on_image(instance)

        instance.save()
