import views

from django.conf.urls import url

urlpatterns = [
    url(r'^orders/$', views.OrderListView.as_view(), name='order-list'),
    url(r'^orders/~(?P<slug>[a-zA-Z0-9]+)/$',  views.OrderDetailView.as_view(), name="order_detail"),
    url(r'^orders/delete/~(?P<slug>[a-zA-Z0-9]+)/$',  views.OrderDeleteView.as_view(), name="order_delete"),
    url(r'^orders/create/',  views.OrderCreateView.as_view(), name="order_create"),
    url(r'^orders/update/~(?P<slug>[a-zA-Z0-9]+)',  views.OrderUpdateView.as_view(), name="order_update"),

    url(r'^products/~(?P<slug>[a-zA-Z0-9]+)/$',  views.ProductDetailView.as_view(), name="product_detail"),
    url(r'^products/$',  views.ProductListView.as_view(), name="product_list"),

]

