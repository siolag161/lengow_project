# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20151025_0225'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartline',
            name='currency',
            field=models.CharField(default=b'EUR', max_length=20),
        ),
        migrations.AddField(
            model_name='product',
            name='currency',
            field=models.CharField(default=b'EUR', max_length=20),
        ),
    ]
