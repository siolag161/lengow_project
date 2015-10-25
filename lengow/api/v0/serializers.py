from rest_framework import serializers
import apps.orders.models  as models

from rest_framework.exceptions import APIException

class MarketPlaceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.MarketPlace


class AddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Address


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    carts = serializers.HyperlinkedRelatedField(view_name='cartline-detail', many=True, read_only=True)

    class Meta:
        model = models.Product


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    cart = serializers.HyperlinkedRelatedField(view_name='cartline-detail', many=True, read_only=True)

    class Meta:
        model = models.Order

import logging
logger = logging.getLogger('werkzeug')


class CartLineSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.CartLine
        read_only_fields = ('tax_rate', 'unit_price', 'currency')

    def create(self, validated_data):
        logger.critical(validated_data)
        cart_line = super(CartLineSerializer, self).create(validated_data)
        cart_line.order.total_tax += cart_line.total_tax
        cart_line.order.total_price += cart_line.total_price
        cart_line.order.quantity += cart_line.quantity
        cart_line.order.save()
        return cart_line



    def update(self, instance, validated_data):
        cart_line = super(CartLineSerializer, self).update(instance, validated_data)
        cart_line.order.update_values_according_to_cart()
        cart_line.order.save()
        return cart_line
