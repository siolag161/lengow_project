from django.conf.urls import *
from rest_framework.routers import DefaultRouter

import views

router = DefaultRouter()
router.register(r'marketplaces', views.MarketPlaceViewSet)
router.register(r'addresses', views.AddressViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'cartline', views.CartLineViewSet)

urlpatterns = patterns(
    '',
    url(r'^',  include(router.urls)),
)