from django.core.management.base import BaseCommand
from django.db import connection
from enot_app.toolbox import dictfetchall

from enot_app.models import Trip


class Command(BaseCommand):
    """ Force rating on trips"""

    def handle(self, *args, **options):
        pass
        # cursor = connection.cursor()
        # query = """
        #         SELECT id,
        #                destination_id,
        #                destination_name,
        #                destination_code,
        #                departure_date,
        #                return_date,
        #                distance,
        #                price,
        #                stops,
        #                found_at,
        #                pre_rating,
        #                chd_days
        #         FROM enot_app_bid
        #         GROUP BY destination_name
        #         ORDER BY pre_rating DESC
        #         """
        # cursor.execute(query)
        # bids = dictfetchall(cursor)