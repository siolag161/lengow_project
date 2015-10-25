# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20151025_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(default=apps.orders.models.generate_uuid, max_length=120, serialize=False, editable=False, primary_key=True),
        ),
    ]
