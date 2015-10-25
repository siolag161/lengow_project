# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.sites.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_set_site_domain_and_name'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='site',
            managers=[
                ('objects', django.contrib.sites.models.SiteManager()),
            ],
        ),
        migrations.AlterField(
            model_name='site',
            name='domain',
            field=models.CharField(max_length=100, verbose_name='domain name', validators=[django.contrib.sites.models._simple_domain_name_validator]),
        ),
        migrations.AlterField(
            model_name='site',
            name='name',
            field=models.CharField(max_length=50, verbose_name='display name'),
        ),
    ]
