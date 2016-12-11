# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0003_auto_20161210_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='processing_output_info',
            field=models.CharField(max_length=255, verbose_name='Processing info output', blank=True),
        ),
    ]
