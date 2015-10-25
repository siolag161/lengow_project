# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20151025_0525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartline',
            name='product',
            field=models.ForeignKey(related_name='carts', to='orders.Product'),
        ),
    ]
