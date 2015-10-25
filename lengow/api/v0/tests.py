import json
from decimal import Decimal

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

import apps.orders.models as models


class CRUDTestCases(APITestCase):

    def test_create_get_marketplace(self):
        url = reverse('api:marketplace-list')
        data = {'name': 'Paypal'}
        response = self.client.post(url, data, format='json')  # creates
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.MarketPlace.objects.count(), 1)
        self.assertEqual(models.MarketPlace.objects.get().name, 'Paypal')

        response = self.client.get(url, data, format='json')  # retrieves
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)[0]
        self.assertEqual(response_data['name'], 'Paypal')

    def test_CRUD_address(self):
        list_url = reverse('api:address-list')
        data = {'first_name': 'David', 'last_name': 'John', 'email': 'a@a.com',
                 'address1': '123 rue de la Forge', 'city': 'Nantes', 'country': 'Fr',
                 'zip_code': '44100', 'phone': '0101020304'}

        response = self.client.post(list_url, data, format='json')  # creates
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Address.objects.count(), 1)
        self.assertEqual(models.Address.objects.get().phone, '0101020304')

        response = self.client.get(list_url, data, format='json') # retrieves
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)[0]
        self.assertEqual(response_data['address1'], '123 rue de la Forge')

        print response_data['url']
        data['first_name'] = 'Robert'
        detail_url = response_data['url']  # update
        response = self.client.put(detail_url, data, format='json')  # update
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(detail_url, data, format='json') # retrieves
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['first_name'], 'Robert')

        self.assertEqual(models.Address.objects.count(), 1)
        response = self.client.delete(detail_url, data, format='json')  # delete
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Address.objects.count(), 0)

    def test_CRUD_product(self):
        list_url = reverse('api:product-list')
        data = {'sku': 'ip38djdososo', 'id_lengow': '3843903404', 'title': 'iphone 4 6GO',
                'category': 'Informatique > Phones',
                'brand': 'Apple', 'unit_price':  500, 'tax_rate': 0.20, 'currency': 'EUR',
                'image_url': 'http://pmcdn.priceminister.com/photo/Iphone-4s-8-Go-1042782025_L.jpg', }

        response = self.client.post(list_url, data, format='json')  # creates
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Product.objects.count(), 1)
        self.assertEqual(models.Product.objects.get().brand, 'Apple')

        response = self.client.get(list_url, data, format='json') # retrieves
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)[0]
        self.assertEqual(response_data['image_url'],
                         'http://pmcdn.priceminister.com/photo/Iphone-4s-8-Go-1042782025_L.jpg')

        detail_url = response_data['url']  # update read-only
        data['tax_rate'] = 0.18
        response = self.client.put(detail_url, data, format='json')  # update
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(detail_url, data, format='json') # retrieves
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.assertAlmostEqual(Decimal(response_data['tax_rate']), Decimal(0.18))

        self.assertEqual(models.Product.objects.count(), 1)
        response = self.client.delete(detail_url, data, format='json')  # delete
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Product.objects.count(), 0)

    def test_CRUD_orders(self):  # a bit messy, have no time, under huge deadline
        adr_url = reverse('api:address-list')
        adr_data = {'first_name': 'David', 'last_name': 'John', 'email': 'a@a.com',
                    'address1': '123 rue de la Forge', 'city': 'Nantes', 'country': 'Fr',
                    'zip_code': '44100', 'phone': '0101020304'}
        adr_response = json.loads(self.client.post(adr_url, adr_data, format='json').content)  # creates

        market_url = reverse('api:marketplace-list')
        market_data = {'name' : 'PriceMinister'}
        market_response = json.loads(self.client.post(market_url, market_data, format='json').content)

        order_url = reverse('api:order-list')
        order_data = {'delivery_address': adr_response['url'], 'marketplace': market_response['url'],
                      'commission_fees': 20.5, 'processing_fees': 30.5,}
        order_response = self.client.post(order_url, order_data, format='json')  # creates

        # should be 400 bad request

        self.assertEqual(order_response.status_code, status.HTTP_201_CREATED)
        order_data = json.loads(order_response.content)

        self.assertAlmostEqual(Decimal(order_data['commission_fees']), Decimal(20.5))
        self.assertAlmostEqual(Decimal(order_data['processing_fees']), Decimal(30.5))

    def test_CRUD_cartline(self):
        product_list_url = reverse('api:product-list')
        product_data = {'sku': 'ip38djdososo', 'id_lengow': '3843903404', 'title': 'iphone 4 6GO',
                'category': 'Informatique > Phones',
                'brand': 'Apple', 'unit_price':  500, 'tax_rate': 0.20, 'currency': 'EUR',
                'image_url': 'http://pmcdn.priceminister.com/photo/Iphone-4s-8-Go-1042782025_L.jpg', }

        product_response = self.client.post(product_list_url, product_data, format='json')  # creates
        product_res_data = json.loads(product_response.content)

        adr_url = reverse('api:address-list')
        adr_data = {'first_name': 'David', 'last_name': 'John', 'email': 'a@a.com',
                    'address1': '123 rue de la Forge', 'city': 'Nantes', 'country': 'Fr',
                    'zip_code': '44100', 'phone': '0101020304'}
        adr_response = json.loads(self.client.post(adr_url, adr_data, format='json').content)  # creates

        market_url = reverse('api:marketplace-list')
        market_data = {'name' : 'PriceMinister'}
        market_response = json.loads(self.client.post(market_url, market_data, format='json').content)

        order_url = reverse('api:order-list')
        order_data = {'delivery_address': adr_response['url'], 'marketplace': market_response['url'],
                      'commission_fees': 20.5, 'processing_fees': 30.5,}
        order_res_data = json.loads(self.client.post(order_url, order_data, format='json').content)  # creates

        cartline_url = reverse('api:cartline-list')
        cartline_data = {'quantity': 4, 'product' : product_res_data['url'], 'order' : order_res_data['url']}
        cartline_res = self.client.post(cartline_url, cartline_data, format='json')
        # should be: created with success
        self.assertEqual(cartline_res.status_code, status.HTTP_201_CREATED)

        # do it again: should be: 400 (already in the db)
        cartline_res = self.client.post(cartline_url, cartline_data, format='json')
        # should be: created with success
        self.assertEqual(cartline_res.status_code, status.HTTP_400_BAD_REQUEST)


class FilterTestCases(APITestCase):
    pass

