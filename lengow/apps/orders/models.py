# -*- coding: UTF-8 -*-

import shortuuid
from decimal import Decimal

from django.utils.encoding import (python_2_unicode_compatible,)
from django.db import models
from django_enumfield import enum
from django.utils import timezone

from .fields import (MarketplaceStatus, LengowStatus)

import logging
logger = logging.getLogger('werkzeug')


def hash_string(val):
    import base64
    return base64.urlsafe_b64encode(val)


def generate_uuid():
    return shortuuid.uuid()


@python_2_unicode_compatible
class Order(models.Model):
    """
    The idea is that the information of this model depends on t
    """
    order_id = models.CharField(max_length=32, primary_key=True, editable=False, default=generate_uuid)
    lengow_status = enum.EnumField(LengowStatus, default=LengowStatus.NEW)
    marketplace_status = enum.EnumField(MarketplaceStatus, default=MarketplaceStatus.VALIDATED_FIANET)
    purchase_date = models.DateTimeField(default=timezone.now, editable=False, )
    shipping_fees = models.DecimalField(max_digits=20, decimal_places=4,  default=Decimal(0.0))
    commission_fees = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal(0.0))
    processing_fees = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal(0.0))
    currency = models.CharField(max_length=20, default="EUR")
    delivery_address = models.ForeignKey('orders.Address')
    marketplace = models.ForeignKey('orders.MarketPlace')
    hashed_id = models.SlugField(max_length=32, unique=True, editable=False, default=generate_uuid)

    #  denormalization
    total_price = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal(0.0, ),
                                      editable=False,)  # easier for filtering
    total_tax = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal(0.0),
                                    editable=False,)  # easier for filtering

    quantity = models.IntegerField(default=0, editable=False,)  # easier for filtering

    def add_product(self, product, quantity):  # assumes quantity > 0,
        """
        very naive way to do
        """
        if quantity <= 0:
            return

        cartline, created = CartLine.objects.get_or_create(product=product, order=self)
        price = cartline.unit_price*quantity
        tax = cartline.tax_rate*price

        if not created:
            cartline.quantity += quantity
        else:
            cartline.quantity = quantity

        self.total_price += price
        self.total_tax += tax
        self.quantity += quantity
        cartline.save()

    def remove_product(self, product, q):
        if q <= 0:
            return

        cartline = CartLine.objects.get(product=product, order=self)
        price = cartline.unit_price*q
        tax = cartline.tax_rate*price
        if cartline and cartline.quantity >= q:
            cartline.quantity -= q
            self.total_price -= price
            self.total_tax -= tax
            self.quantity -= q
            cartline.save()

    def __str__(self):
        return u"%s-%s" % (self.delivery_address, self.order_id)

    def compute_total_tax_from_carts(self):
        items = self.cart.all()
        self.total_tax = sum(item.total_tax for item in items) if items else 0
        return self.total_tax

    def compute_quantity_from_carts(self):
        items = self.cart.all()
        self.quantity = sum(item.quantity for item in items) if items else 0
        return self.quantity

    def compute_total_price_from_carts(self):
        items = self.cart.all()
        self.total_price = sum(item.total_price for item in items) if items else 0
        return self.total_price

    def update_values_according_to_cart(self):
        self.compute_total_tax_from_carts()
        self.compute_quantity_from_carts()
        self.compute_total_price_from_carts()

    @property
    def total_amount(self):
        elements = [self.total_price, self.total_tax, self.shipping_fees, self.processing_fees, self.commission_fees]
        return sum(elem for elem in elements if elem)

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

    @property
    def day_of_purchase(self):
        return self.purchase_date.date()

    @models.permalink
    def get_absolute_url(self):
        return 'order_detail', (), {'slug': self.hashed_id}


@python_2_unicode_compatible
class MarketPlace(models.Model):
    name = models.CharField(max_length=128, null=False)
    marketplace_id = models.CharField(max_length=32, null=False, primary_key=True, default=generate_uuid)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Product(models.Model):
    """
    @todo: cleans the data (for example remove double space)
    """
    # @todo not sure if true for each market or true globally
    sku = models.CharField(max_length=120, primary_key=True, editable=False, default=generate_uuid)

    id_lengow = models.CharField(max_length=40, null=False, editable=False, unique=True, default=generate_uuid)
    title = models.CharField(max_length=80)
    brand = models.CharField(max_length=40, default="", blank=True, null=True)
    category = models.TextField()  # should be a tree like MP_Tree or something, for now A->B->C

    unit_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.0)
    tax_rate = models.DecimalField(max_digits=20, decimal_places=4, default=0.0)
    image_url = models.URLField(blank=True, null=True)
    currency = models.CharField(max_length=20, default="EUR")

    def __str__(self):
        elems = [self.title, self.brand, self.category]
        return u" ".join(elem for elem in elems if elem)

    @models.permalink
    def get_absolute_url(self):
        return 'product_detail', (), {'slug': self.id_lengow}


@python_2_unicode_compatible
class CartLine(models.Model):
    """
    unit price = price at the time of adding the product to this product_line
    """
    product = models.ForeignKey("orders.Product", related_name='carts')
    order = models.ForeignKey("orders.Order", related_name='cart')

    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.0)  # @todo: explains
    tax_rate = models.DecimalField(max_digits=20, decimal_places=4, default=0.0)  # @todo: explains
    currency = models.CharField(max_length=20, default="EUR")

    def __str__(self):
        s = u"%s (Price: %.2f, Tax: %.2f, Qty: %s)" % (self.product, self.unit_price, self.tax_rate, self.quantity)
        return s

    class Meta:
        unique_together = ('product', 'order', 'unit_price', 'tax_rate')

    def save(self, *args, **kwargs):
        if self.pk is not None and hasattr(self, 'product'):
            orig = CartLine.objects.get(pk=self.pk)
            if orig.product.pk != self.product.pk:
                self.unit_price = self.product.unit_price
                self.tax_rate = self.product.tax_rate
                self.currency = self.product.currency
        else:
            if not self.unit_price and hasattr(self, 'product'):
                self.unit_price = self.product.unit_price
            if not self.tax_rate and hasattr(self, 'product'):
                self.tax_rate = self.product.tax_rate
            if not self.currency and self.product.currency:
                self.currency = self.product.currency

        super(CartLine, self).save(*args, **kwargs)

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    @property
    def total_tax(self):
        return self.tax_rate*self.total_price


@python_2_unicode_compatible
class Address(models.Model):
    first_name = models.CharField(max_length=60, default="", blank=True, null=True)
    last_name = models.CharField(max_length=60, default="", blank=True, null=True)
    email = models.EmailField(null=True)
    address1 = models.CharField(max_length=120, default="", blank=True, null=True)
    city = models.CharField(max_length=40, default="", blank=True, null=True)
    country = models.CharField(max_length=40, default="", blank=True, null=True)
    zip_code = models.CharField(max_length=40, default="", blank=True, null=True)
    phone = models.CharField(max_length=40, default="", blank=True,
                             null=True)  # there will be no validation for this field

    @property
    def fullname(self):
        """
        :rtype : object
        """
        name_elems = [self.first_name, self.last_name]
        return u" ".join(elem for elem in name_elems if elem)

    @property
    def full_address(self):
        adr_elems = [self.address1, self.zip_code, self.city, self.country]
        return u" ".join(elem for elem in adr_elems if elem)

    def __str__(self):
        infos = [self.fullname, self.email, self.phone, self.full_address]
        return u", ".join(info for info in infos if info and info.strip() != '')
