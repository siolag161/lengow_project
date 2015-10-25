# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20151024_2201'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartline',
            unique_together=set([('product', 'order', 'unit_price', 'tax_rate')]),
        ),
    ]
