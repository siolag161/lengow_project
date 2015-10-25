from django.conf.urls import url, include

from .views import (OrderListView, OrderDetailView, OrderDeleteView, OrderCreateView, OrderUpdateView)

from django.conf.urls import url

urlpatterns = [
    url(r'^orders/$', OrderListView.as_view(), name='order-list'),
    url(r'^orders/~(?P<slug>[a-zA-Z0-9]+)/$', OrderDetailView.as_view(), name="order_detail"),
    url(r'^orders/delete/~(?P<slug>[a-zA-Z0-9]+)/$', OrderDeleteView.as_view(), name="order_delete"),
    url(r'^orders/create/', OrderCreateView.as_view(), name="order_create"),
    url(r'^orders/update/~(?P<slug>[a-zA-Z0-9]+)', OrderUpdateView.as_view(), name="order_update"),

]

