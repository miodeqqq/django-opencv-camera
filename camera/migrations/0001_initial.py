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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(verbose_name='Image title', max_length=255)),
                ('image', models.ImageField(blank=True, upload_to=camera.models.upload_images_path, verbose_name='Image file', null=True)),
            ],
            options={
                'verbose_name_plural': 'Images',
                'verbose_name': 'Image',
            },
        ),
    ]
