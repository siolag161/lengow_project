# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20151025_0536'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(default=Decimal('0'), editable=False, max_digits=20, decimal_places=4),
        ),
        migrations.AddField(
            model_name='order',
            name='total_tax',
            field=models.DecimalField(default=Decimal('0'), editable=False, max_digits=20, decimal_places=4),
        ),
    ]
