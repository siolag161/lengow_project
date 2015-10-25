# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20151024_0400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_tax',
        ),
        migrations.AlterField(
            model_name='cartline',
            name='order',
            field=models.ForeignKey(related_name='cart', to='orders.Order'),
        ),
        migrations.AlterField(
            model_name='order',
            name='marketplace',
            field=models.ForeignKey(to='orders.MarketPlace'),
        ),
    ]
