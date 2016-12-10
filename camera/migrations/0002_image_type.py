# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camera', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='type',
            field=models.BooleanField(default='', help_text='0 - face recognition, 1 - eyes recognition', verbose_name='Type of processing', choices=[(0, 'Face recognition'), (1, 'Eyes recognition')]),
            preserve_default=False,
        ),
    ]
