# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import camera.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='Image title', max_length=255)),
                ('image', models.ImageField(verbose_name='Image file', blank=True, upload_to=camera.models.upload_images_path, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
    ]
