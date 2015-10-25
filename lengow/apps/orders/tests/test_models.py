from decimal import Decimal
from django.test import TestCase

from ..models import (Address, Product, CartLine, Order, MarketPlace, hash_string)
from ..fields import (MarketplaceStatus, LengowStatus)

from ..factories import (AddressFactory, ProductFactory, CartLineFactory, OrderFactory, MarketPlaceFactory)


class AddressTestCase(TestCase):
    def test_address_factory(self):
        AddressFactory.create()
        count = Address.objects.count()
        self.assertEqual(count, 1)

    def test_address_factory_multiple(self):
        count = 10
        adrs = AddressFactory.create_batch(count)
        self.assertEqual(count, Address.objects.count())
        self.assertEqual(len(adrs), count)

    def test_address_bill_fullname(self):
        count = 10
        adrs = AddressFactory.create_batch(count)
        for i, adr in enumerate(adrs):
            full_name = adr.fullname
            self.assertEqual(full_name, "Tom_%s Phan_%s" % (i, i))

    def test_address_fulladdress(self):
        adr = AddressFactory(city="Paris")
        self.assertEqual(adr.full_address, "%s %s Paris %s" % (adr.address1, adr.zip_code, adr.country))


class ProductTestCase(TestCase):
    def test_product_factory(self):
        prd = ProductFactory.create(unit_price=10)
        self.assertEqual(prd.unit_price, 10.0)
        prd, _ = Product.objects.get_or_create(sku="123")
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(prd.sku, "123")

    def test_product_factory_multiple(self):
        count = 29
        products = ProductFactory.create_batch(count)
        total_price = sum(prd.unit_price for prd in products)
        self.assertAlmostEqual(total_price, 29.0*(29.0-1)/2*5.35, 5)
        self.assertEqual(Product.objects.count(), count)

    def test_product_category(self):
        prd = ProductFactory.create(unit_price=10)
        self.assertTrue(prd.category.startswith("0 -> 1 -> 2"))

    def test_product_unicity(self):
        # test other pricing strategies
        ProductFactory.create(sku="123")
        # self.assertRaises(IntegrityError, ProductFactory.create(sku="123"))


class TestUtils(TestCase):
    def test_hash(self):
        a = hash_string("ds,dsds")
        self.assertFalse(',' in a)


class CartLineTestCase(TestCase):
    def setUp(self):
        self.products = ProductFactory.create_batch(10, unit_price=3.5)
        self.orders = OrderFactory.create_batch(10)

    def test_cart_line_factory_default(self):
        cartline = CartLineFactory.create(product=self.products[0], order=self.orders[0], quantity=0)
        self.assertEqual(cartline.quantity, 0)
        self.assertEqual(cartline.unit_price, Decimal(3.5))
        self.assertEqual(cartline.total_price, Decimal(0.0))

    def test_unique_together(self):
        cartline = CartLineFactory.create(product=self.products[0], order=self.orders[0], quantity=0)
        cl = CartLine.objects.get(product=self.products[0], order=self.orders[0])
        self.assertEqual(cartline.pk, cl.pk)

    def test_cart_line_factory_basc(self):
        cartline = CartLineFactory.create(product=self.products[0], order=self.orders[0], quantity=3)
        self.assertEqual(cartline.quantity, 3)
        self.assertEqual(cartline.unit_price, Decimal(3.5))
        self.assertEqual(cartline.total_price, Decimal(3.5*3))


class OrderTestCase(TestCase):
    def setUp(self):
        self.products = [ProductFactory.create(unit_price=Decimal(i+1)) for i in range(4)]

    def test_order_default(self):
        self.order = OrderFactory.create()
        self.assertEqual(Order.objects.count(), 1)
        self.assertAlmostEqual(self.order.total_price, Decimal(0.0))
        self.assertAlmostEqual(self.order.total_tax, Decimal(0.0))
        self.assertAlmostEqual(self.order.total_amount, Decimal(4.9))
        self.assertEqual(self.order.currency, "EUR")

    def test_order_status(self):
        self.order = OrderFactory.create()
        self.order.lengow_status = MarketplaceStatus.invert_label("ValidatedFianet")
        self.order.save()
        self.assertEqual(self.order.lengow_status, MarketplaceStatus.VALIDATED_FIANET)

    def test_add_product(self):
        self.order = OrderFactory.create()
        self.assertEqual(self.order.quantity, 0)
        self.order.add_product(self.products[0], 1)
        self.order.add_product(self.products[0], 1)
        self.order.add_product(self.products[0], 1)
        self.assertEqual(self.order.quantity, 3)

        o = Order.objects.get(pk=self.order.pk)
        self.assertEqual(o.quantity, 0) # not yet updated
        self.order.save()

        o = Order.objects.get(pk=self.order.pk)
        self.assertEqual(o.quantity, 3) # not yet updated

        self.order.add_product(self.products[1], 21)
        self.order.save()
        o = Order.objects.get(pk=self.order.pk)
        self.assertEqual(o.quantity, 24)
        self.assertEqual(o.total_price, Decimal(21*self.products[1].unit_price + 3*self.products[0].unit_price))

    def test_remove_product(self):
        self.order = OrderFactory.create()
        self.order.add_product(self.products[0], 3)
        self.order.save()

        o = Order.objects.get(pk=self.order.pk)
        self.assertEqual(o.quantity, 3)
        self.order.remove_product(self.products[0], 1)
        self.order.save()
        o = Order.objects.get(pk=self.order.pk)
        self.assertEqual(o.quantity, 2)

        self.order.remove_product(self.products[0], 2, save=0)
        self.order.save()
        o = Order.objects.get(pk=self.order.pk)
        self.assertEqual(o.quantity, 0)


class MarketPlaceTestCase(TestCase):
    def test_create(self):
        mk = MarketPlaceFactory.create(name="amazon")
        self.assertEqual(MarketPlace.objects.count(), 1)