# -*- coding: utf-8 -*-

from decimal import Decimal
from collections import OrderedDict
import xmltodict
from django.test import TestCase

from ..models import (Address, Product, MarketPlace, Order, CartLine)
from ..fields import (MarketplaceStatus, LengowStatus)
from ..tasks import LengowOrderXMLParser as XMLParser
from ..factories import (OrderFactory)


class TestRetrieveXML(TestCase):
    @classmethod
    def remove_double(cls, s):
        return " ".join(s.split())

    def setUp(self):
        import os
        current_dir = os.path.dirname(__file__)
        with open(os.path.join(current_dir, 'sample_xml_api_v21.xml'), 'r') as f:
            self.data = f.read()

            self.xml_data = xmltodict.parse(self.data)
            self.order_dicts = XMLParser.to_list(self.xml_data['statistics']['orders']['order'])
            self.order_dict = self.order_dicts[0]

    def test_to_list(self):
        self.assertEqual(XMLParser.to_list('a'), ['a'])
        self.assertEqual(XMLParser.to_list(['a']), ['a'])
        self.assertEqual(XMLParser.to_list({'a': 'a'}), [{'a': 'a'}])
        self.assertEqual(XMLParser.to_list(None), [])

    def test_parsing_xml(self):
        self.assertEqual(len(self.order_dicts), 5)
        self.assertTrue(isinstance(self.order_dict['cart']['products']['product'], OrderedDict))

    def test_getting_marketplace(self):
        mk = XMLParser.get_market_place(self.order_dict)
        self.assertTrue(mk.pk >= 0)
        mk2 = XMLParser.get_market_place(self.order_dict)
        self.assertEqual(mk2, mk)  # not created a new one
        self.assertEqual(MarketPlace.objects.count(), 1)  # not created a new one
        self.assertEqual(mk2.name, "amazon")

        mk3 = XMLParser.get_market_place(self.order_dicts[3])  # should be a new one (cdiscount)
        self.assertNotEqual(mk2.pk, mk3.pk)  # not created a new one
        self.assertEqual(MarketPlace.objects.count(), 2)
        self.assertEqual(mk3.name, "cdiscount")

    def test_getting_address(self):
        adr_dict = self.order_dict['delivery_address']
        adr = XMLParser.get_address(adr_dict)
        self.assertEqual(adr.address1, u'014 rue de la poupée')
        self.assertEqual(adr.zip_code, u'75000')
        self.assertEqual(adr.city, u'Paris')
        self.assertEqual(adr.country, u'FR')
        self.assertEqual(adr.phone, u'0605040102')
        self.assertEqual(adr.full_address, u'014 rue de la poupée 75000 Paris FR')
        full_adr = ' '.join(adr_dict['delivery_full_address'].split())  # removes spaces
        self.assertEqual(adr.full_address, full_adr)

        XMLParser.get_address(adr_dict)
        self.assertEquals(Address.objects.count(), 1)  # should not change

        adr_dict1 = self.order_dicts[1]['delivery_address']
        XMLParser.get_address(adr_dict1)
        self.assertEquals(Address.objects.count(), 2)  # should now change

    def test_get_datetime(self):
        dt = XMLParser.get_purchase_datetime_string(self.order_dict)
        # "2014-10-21 14:59:51")
        self.assertEqual(dt.year, 2014)
        self.assertEqual(dt.month, 10)
        self.assertEqual(dt.day, 21)
        self.assertEqual(dt.hour, 14)
        self.assertEqual(dt.minute, 59)
        self.assertEqual(dt.second, 51)

    def test_get_order_by_id(self):
        order = XMLParser.get_order_by_id('123')
        self.assertTrue(order._state.adding)  # not yet added to the database
        order = OrderFactory.create()
        self.assertFalse(order._state.adding)  # already added to the database

    def test_get_product(self):
        prod_dict = XMLParser.to_list(self.order_dict['cart']['products']['product'])[0]
        self.assertEqual(Product.objects.count(), 0)
        prod = XMLParser.get_product(prod_dict)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(prod.sku, "11_12")
        self.assertEqual(prod.id_lengow, "114526")
        self.assertEqual(self.remove_double(prod.title), "T-Shirt col rond")
        self.assertEqual(prod.image_url, "http://brain.pan.e-merchant.com/3/7/12313673/l_12313673.jpg")
        self.assertEqual(prod.category, "Vetements Femmes > Tee-shirts")
        XMLParser.get_product(prod_dict)
        self.assertEqual(Product.objects.count(), 1)

    def test_retrieve_order(self):
        order_id = self.order_dict['order_id']
        self.assertEqual(order_id, "111-2222222-3333333")
        order = XMLParser.get_order_by_id(order_id)
        self.assertEqual(order_id, order.order_id)

    def test_order(self):
        order = XMLParser.get_order(self.order_dicts[1])
        order.save()
        self.assertEqual(order.order_id, "123-4567890-1112131")
        self.assertEqual(order.lengow_status, LengowStatus.invert_label("processing"))
        self.assertEqual(order.marketplace_status, MarketplaceStatus.invert_label("accept"))

        # supposed_datetime = "2014-10-20 14:59:51"
        self.assertEqual(order.purchase_date.year, 2014)
        self.assertEqual(order.purchase_date.month, 10)
        self.assertEqual(order.purchase_date.day, 20)
        self.assertEqual(order.purchase_date.hour, 14)
        self.assertEqual(order.purchase_date.minute, 59)
        self.assertEqual(order.purchase_date.second, 51)

        self.assertEqual(order.commission_fees, Decimal(0.00))
        self.assertEqual(order.processing_fees, Decimal(0.00))
        self.assertEqual(order.currency, u'EUR')

        self.assertEqual(order.marketplace.name, "amazon")
        self.assertEqual(order.marketplace.marketplace_id, "88827")
        self.assertEqual(order.marketplace.pk, "88827")

        self.assertEqual(order.shipping_fees, Decimal(5.5))
        self.assertEqual(order.total_amount, Decimal(5.5))
        self.assertEqual(order.total_price, Decimal(0.0))

        adr = order.delivery_address
        self.assertEqual(adr.full_address, u"1512 Rue de l'Impasse 44000 Nantes FR")

    def test_cartlines_for_one_order(self):
        order_dict = self.order_dicts[1]
        prod_dict = XMLParser.to_list(order_dict['cart']['products']['product'])[0]
        order_id = self.order_dicts[1]['order_id']
        order = XMLParser.get_order(order_dict)
        order.save()

        prod = XMLParser.get_product(prod_dict)
        cartline = XMLParser.get_cart_line_given_order_product(order_id, prod_dict)
        cartline.save()
        self.assertEqual(CartLine.objects.count(), 1)
        cartline = CartLine.objects.get(pk=cartline.pk)

        self.assertEqual(cartline.quantity, 2)
        self.assertEqual(cartline.unit_price, Decimal(55.0))
        self.assertEqual(cartline.total_price, Decimal(110))
        self.assertEqual(prod.pk, cartline.product.pk)
        self.assertEqual(order.pk, cartline.order.pk)
        self.assertEqual(cartline.product.image_url,
                         "http://csimg.webmarchand.com/srv/FR/29049962bos7121v342010/T/340x340/C/FFFFFF/"
                         "url/jeans-femme-slim-sofia-bonobo.jpg")

        cart_line_given_order = XMLParser.get_cart_line_for_order(order_dict)
        self.assertEqual(len(cart_line_given_order), 1)

    def test_parsing_bulk_orders(self):
        orders = XMLParser.parse_bulk_orders(self.order_dicts)
        self.assertEqual(len(orders), 5)
        self.assertEqual(Order.objects.count(), 0)
        Order.objects.bulk_create(orders)
        self.assertEqual(Order.objects.count(), 5)
        s = sum(order.quantity for order in Order.objects.all())
        self.assertEqual(s, 0)

    def test_parsing_bulk_orderlines(self):
        orders = XMLParser.parse_bulk_orders(self.order_dicts)
        Order.objects.bulk_create(orders)

        cart_lines = XMLParser.parse_bulk_cartlines(self.order_dicts)
        self.assertEqual(CartLine.objects.count(), 0)

        total_quantity = sum(order.quantity for order in Order.objects.all())
        self.assertEqual(total_quantity, 0)  # before saving cartlines
        self.assertEqual(Order.objects.count(), 5)

        CartLine.objects.bulk_create(cart_lines)
        XMLParser.manual_update_orders(orders)
        total_quantity = sum(order.quantity for order in Order.objects.all())
        self.assertEqual(total_quantity, 6)

        self.assertEqual(CartLine.objects.count(), 5)


