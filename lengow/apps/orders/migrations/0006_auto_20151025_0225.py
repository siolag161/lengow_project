# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20151025_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketplace',
            name='marketplace_id',
            field=models.CharField(default=apps.orders.models.generate_uuid, max_length=32, serialize=False, primary_key=True),
        ),
    ]
