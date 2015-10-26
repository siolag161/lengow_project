import json
from django.db.utils import IntegrityError

from rest_framework.permissions import AllowAny
from rest_framework import (viewsets, response, status)

import apps.orders.models as models
import serializers
import filters


class AllowAllMixin(object):

    def get_permissions(self):
        # we don't want to deal with authentification, just want to use, man
        return AllowAny(),


class MarketPlaceViewSet(AllowAllMixin, viewsets.ModelViewSet):
    queryset = models.MarketPlace.objects.all()
    serializer_class = serializers.MarketPlaceSerializer


class AddressViewSet(AllowAllMixin, viewsets.ModelViewSet):
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer


class ProductViewSet(AllowAllMixin, viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class OrderViewSet(AllowAllMixin, viewsets.ModelViewSet):
    queryset = models.Order.objects.all().prefetch_related()  # speeds thing up a bit
    serializer_class = serializers.OrderSerializer
    filter_class = filters.OrderFilter


class CartLineViewSet(AllowAllMixin, viewsets.ModelViewSet):
    queryset = models.CartLine.objects.all()
    serializer_class = serializers.CartLineSerializer

    def create(self, request, *args, **kwargs):
        """
        Try to create a cartline if not exists already (product,order,unit_price)
        Returns 201 or 400 if created and not, respectively.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError as e:
            res = {"code": status.HTTP_400_BAD_REQUEST, "message": "Bad Requset", "errors": e.message}
            return response.Response(data=json.dumps(res), status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        cart_line = self.get_object()
        cart_line.order.update_values_according_to_cart()
        cart_line.order.save()
        return super(CartLineViewSet, self).destroy(request, *args, **kwargs)
