# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20151024_0337'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartline',
            unique_together=set([('product', 'order')]),
        ),
    ]
