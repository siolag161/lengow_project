# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from decimal import Decimal
import apps.orders.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(default=b'', max_length=60, null=True, blank=True)),
                ('last_name', models.CharField(default=b'', max_length=60, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('address1', models.CharField(default=b'', max_length=120, null=True, blank=True)),
                ('city', models.CharField(default=b'', max_length=40, null=True, blank=True)),
                ('country', models.CharField(default=b'', max_length=40, null=True, blank=True)),
                ('zip_code', models.CharField(default=b'', max_length=40, null=True, blank=True)),
                ('phone', models.CharField(default=b'', max_length=40, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CartLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=1)),
                ('unit_price', models.DecimalField(default=0.0, max_digits=20, decimal_places=4)),
                ('tax_rate', models.DecimalField(default=0.0, max_digits=20, decimal_places=4)),
            ],
        ),
        migrations.CreateModel(
            name='MarketPlace',
            fields=[
                ('name', models.CharField(max_length=128)),
                ('marketplace_id', models.CharField(max_length=32, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.CharField(default=apps.orders.models.generate_uuid, max_length=32, serialize=False, editable=False, primary_key=True)),
                ('lengow_status', models.IntegerField(default=1)),
                ('marketplace_status', models.IntegerField(default=1)),
                ('purchase_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('total_price', models.DecimalField(default=Decimal('0'), editable=False, max_digits=20, decimal_places=4)),
                ('total_tax', models.DecimalField(default=Decimal('0'), editable=False, max_digits=20, decimal_places=4)),
                ('shipping_fees', models.DecimalField(default=Decimal('0'), max_digits=20, decimal_places=4)),
                ('commission_fees', models.DecimalField(default=Decimal('0'), max_digits=20, decimal_places=4)),
                ('processing_fees', models.DecimalField(default=Decimal('0'), max_digits=20, decimal_places=4)),
                ('currency', models.CharField(default=b'EUR', max_length=20)),
                ('quantity', models.IntegerField(default=0)),
                ('hashed_id', models.SlugField(default=apps.orders.models.generate_uuid, unique=True, max_length=32, editable=False)),
                ('delivery_address', models.ForeignKey(to='orders.Address')),
                ('marketplace', models.ForeignKey(editable=False, to='orders.MarketPlace')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('sku', models.CharField(max_length=120, serialize=False, editable=False, primary_key=True)),
                ('id_lengow', models.CharField(unique=True, max_length=40, editable=False)),
                ('title', models.CharField(max_length=80)),
                ('brand', models.CharField(default=b'', max_length=40, null=True, blank=True)),
                ('category', models.TextField()),
                ('unit_price', models.DecimalField(default=0.0, max_digits=20, decimal_places=4)),
                ('tax_rate', models.DecimalField(default=0.0, max_digits=20, decimal_places=4)),
                ('image_url', models.URLField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='cartline',
            name='order',
            field=models.ForeignKey(to='orders.Order'),
        ),
        migrations.AddField(
            model_name='cartline',
            name='product',
            field=models.ForeignKey(to='orders.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='cartline',
            unique_together=set([('product', 'order', 'unit_price')]),
        ),
    ]
