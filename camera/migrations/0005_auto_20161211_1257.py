# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import camera.models


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0004_image_processing_output_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image',
        ),
        migrations.AddField(
            model_name='image',
            name='input_image',
            field=models.ImageField(upload_to=camera.models.upload_images_path, null=True, verbose_name='Input image', blank=True),
        ),
        migrations.AddField(
            model_name='image',
            name='output_image',
            field=models.ImageField(upload_to=camera.models.upload_images_path, null=True, verbose_name='Output image', blank=True),
        ),
    ]
