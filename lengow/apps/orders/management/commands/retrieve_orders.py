
import requests
from django.core.management.base import BaseCommand

from ...utils import LengowOrderXMLParser as XMLParser
from ...models import (Order,)

DEFAULT_SOURCE_URL = "http://test.lengow.io/orders-test.xml"  # move to settings perhaps?


class Command(BaseCommand):
    help = 'Retrieves Order as a XML file from a distance source'

    def add_arguments(self, parser):
        parser.add_argument('--url', help='URL of the source', default=DEFAULT_SOURCE_URL)

    def handle(self, *args, **options):
        url = options.get("url")
        res = requests.get(url)

        res.encoding = 'utf-8'
        if res.status_code == 200:
            self.stdout.write("It's Ok. Getting the data fro"
                              "m %s\n" % (url,))
            orders = XMLParser.parse_and_save(res.text)
            self.stdout.write("%s orders passed and saved with success.\n" % (len(orders),))
            self.stdout.write("Done!\n")
        else:
            self.stderr.write("Error from reading from source: %s with code: %s\n" %(url, res.status_code))
