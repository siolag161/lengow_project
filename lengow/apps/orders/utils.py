#
# from decimal import Decimal
# import pytz
# import datetime
# from django.conf import settings
# from django.utils import timezone
# from django.db import transaction
#
# import xmltodict
#
# from .models import (Address, Product, CartLine, MarketPlace, Order)
# from .fields import (MarketplaceStatus, LengowStatus)
#
#
# class LengowOrderXMLParser(object):
#
#     @classmethod
#     def zero_if_null(cls, val):
#         return Decimal(val) if val is not None else Decimal(0.0)
#
#     @classmethod
#     def to_list(cls, val=None):
#         """
#         Deals with XMLToPython's annoying feature: makes sure always working with list.
#         See: https://github.com/martinblech/xmltodict/issues/14
#         """
#         if val is None:
#             return []
#         return val if isinstance(val, list) else [val]
#
#     @classmethod
#     def get_market_place(cls, order_dict):
#         name = order_dict['marketplace']
#         idd = order_dict['idFlux']  # @todo: is correct?
#         marketplace, created = MarketPlace.objects.get_or_create(marketplace_id=idd, name=name)
#         if not created and marketplace.name != name:
#             marketplace.name = name
#             marketplace.save()
#         return marketplace
#
#     @classmethod
#     def get_address(cls, adr_dict):
#         """ should maybe add an index? """
#         email = adr_dict['delivery_email']
#         adr1 = adr_dict['delivery_address']
#         zipcode = adr_dict['delivery_zipcode']
#         city = adr_dict['delivery_city']
#         country = adr_dict['delivery_country']
#         first_name = adr_dict['delivery_firstname']
#         last_name = adr_dict['delivery_lastname']
#         phone = adr_dict['delivery_phone_home']
#         adr, _ = Address.objects.get_or_create(first_name=first_name, last_name=last_name, city=city, phone=phone,
#                                                country=country, zip_code=zipcode, address1=adr1, email=email)
#         return adr
#
#     @classmethod
#     def get_order_by_id(cls, order_id):
#         try:
#             order = Order.objects.get(order_id=order_id)
#         except Order.DoesNotExist:
#             order = Order(order_id=order_id)
#         return order
#
#     @classmethod
#     def get_purchase_datetime_string(cls, d):
#         year, month, day, hour, minute, second = None, None, None, None, None, None
#         purchase_date = d['order_purchase_date']
#         purchase_time = d['order_purchase_heure']
#         if purchase_date:
#             year, month, day = [int(n) for n in purchase_date.split("-")]
#         if purchase_time:
#             hour, minute, second = [int(n) for n in purchase_time.split(":")]
#         if not purchase_date and not purchase_time:
#             dt = timezone.now()
#         else:
#             dt = datetime.datetime(year, month, day, hour, minute, second)
#             dt = pytz.timezone(settings.TIME_ZONE).localize(dt)
#         return dt
#
#     @classmethod
#     def get_product(cls, prod_dict):
#         sku = prod_dict['sku']['#text']
#         product, created = Product.objects.get_or_create(sku=sku)
#         if created:
#             product.id_lengow = prod_dict['idLengow']
#             product.title = prod_dict['title']
#             product.category = prod_dict['category']
#             product.image_url = prod_dict['url_image']
#             product.brand = prod_dict['brand']
#             product.unit_price = cls.zero_if_null(prod_dict['price_unit'])
#             product.tax_rate = cls.zero_if_null(prod_dict['tax'])
#         product.save()
#         return product
#
#     @classmethod
#     def get_order(cls, order_dict):
#         order_id = order_dict['order_id']
#         order = cls.get_order_by_id(order_id)
#         status_dict = order_dict['order_status']
#         order.lengow_status = LengowStatus.invert_label(status_dict['lengow'])
#         order.marketplace_status = MarketplaceStatus.invert_label(status_dict['lengow'])
#         order.purchase_date = cls.get_purchase_datetime_string(order_dict)
#         order.marketplace = cls.get_market_place(order_dict)
#         order.marketplace_status = MarketplaceStatus.invert_label(status_dict["marketplace"])
#         order.shipping_fees = cls.zero_if_null(order_dict['order_shipping'])
#         order.commission_fees = cls.zero_if_null(order_dict['order_commission'])
#         order.processing_fee = cls.zero_if_null(order_dict['order_processing_fee'])
#         order.currency = order_dict['order_currency']  # todo: max = 3
#         order.delivery_address = cls.get_address(order_dict['delivery_address'])
#         return order
#
#     @classmethod
#     def get_cart_line_for_order(cls, order_dict):
#         prod_dicts = cls.to_list(order_dict['cart']['products']['product'])
#         order_id = order_dict['order_id']
#         return [cls.get_cart_line_given_order_product(order_id, prod_dict) for prod_dict in prod_dicts]
#
#     @classmethod
#     def get_cart_line_given_order_product(cls, order_id, prod_dict):
#         quantity = int(prod_dict['quantity']) if prod_dict['quantity'] is not None else 0
#         unit_price = cls.zero_if_null(prod_dict['price_unit'])
#         tax_rate = cls.zero_if_null(prod_dict['tax'])
#         cart_line = CartLine(quantity=quantity, unit_price=unit_price, tax_rate=tax_rate)
#         cart_line.order_id = order_id
#         cart_line.product = cls.get_product(prod_dict)
#         return cart_line
#
#     @classmethod
#     def parse_bulk_orders(cls, order_dicts):
#         return [cls.get_order(order_dict) for order_dict in order_dicts]
#
#     @classmethod
#     def parse_bulk_cartlines(cls, order_dicts):
#         import itertools
#         cart_lines = (cls.get_cart_line_for_order(order_dict) for order_dict in order_dicts)
#         return list(itertools.chain.from_iterable(cart_lines))
#
#     @classmethod
#     def parse_and_save(cls, xml):
#         data = xmltodict.parse(xml, encoding='utf-8')
#         order_dicts = cls.to_list(data['statistics']['orders']['order'])
#         orders = cls.parse_bulk_orders(order_dicts)
#         Order.objects.bulk_create(orders)
#         cart_lines = cls.parse_bulk_cartlines(order_dicts)
#         CartLine.objects.bulk_create(cart_lines)
#         cls.manual_update_orders(orders)
#         return orders
#
#     @classmethod
#     def manual_update_orders(cls, orders=None):
#         orders = orders or Order.objects.all()
#         with transaction.atomic():
#             for order in orders:
#                 order.quantity = 10
#                 order.update_values_according_to_cart()
#                 order.save()
#
