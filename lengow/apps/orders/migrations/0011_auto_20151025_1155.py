# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20151025_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='id_lengow',
            field=models.CharField(default=apps.orders.models.generate_uuid, unique=True, max_length=40, editable=False),
        ),
    ]
