from decimal import Decimal
from factory import LazyAttributeSequence, Sequence, SubFactory
from factory.django import DjangoModelFactory

from .models import (Address, Product, CartLine, MarketPlace, Order)


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    first_name = Sequence(lambda n: 'Tom_%s' % n)
    last_name = Sequence(lambda n: 'Phan_%s' % n)
    email = LazyAttributeSequence(
        lambda o, n: '%s_%s@lengow.io' % (o.first_name.split()[0].lower(), o.last_name.lower()))
    address1 = Sequence(lambda n: '%s rue albert einstein' % n)
    city = "Nantes"
    country = "France"
    zip_code = "44000"
    phone = Sequence(lambda n: '+%s-0652734709' % n)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    id_lengow = Sequence(lambda n: '%d-lengow' % n)
    title = Sequence(lambda n: 'Chemise_%s' % n)
    brand = Sequence(lambda n: 'Ralph Lauren %s' % n)
    sku = Sequence(lambda n: 'rl_%s' % n)
    unit_price = Sequence(lambda n: (n % 29) * 5.35)
    category = Sequence(lambda n: ' -> '.join(str(i) for i in range(n+3)))  # 0->1->2 etc...
    image_url = "google.com/chiot.jpeg"
    tax_rate = Sequence(lambda n: Decimal(n)/Decimal(n+1)*Decimal(0.2))


class CartLineFactory(DjangoModelFactory):
    class Meta:
        model = CartLine

    quantity = Sequence(lambda n : (n+1))
    product = SubFactory(ProductFactory)
    order = SubFactory(CartLine)


class MarketPlaceFactory(DjangoModelFactory):
    class Meta:
        model = MarketPlace
    name = Sequence(lambda n: "super-shop-%d" %(n))
    marketplace_id = Sequence(lambda n: "mk-id-%d" %(n))

class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    order_id = Sequence(lambda n: 'order-%d' % n)
    shipping_fees = Decimal(1.0)
    processing_fees = Decimal(2.40)
    commission_fees = Decimal(1.5)
    currency = "EUR"
    delivery_address = SubFactory(AddressFactory)
    marketplace = SubFactory(MarketPlaceFactory)
