from django.core.management.base import BaseCommand
import django_rq
from rq import Queue, Worker

from ...tasks import parse_orders_from_xml

DEFAULT_SOURCE_URL = "http://test.lengow.io/orders-test.xml"  # move to settings perhaps?


class Command(BaseCommand):
    def handle(self, *args, **options):
        redis_conn = django_rq.get_connection('default')
        q = Queue(connection=redis_conn)
        q.enqueue(parse_orders_from_xml, DEFAULT_SOURCE_URL)
        worker = Worker([q],  connection=redis_conn)
        worker.work()
