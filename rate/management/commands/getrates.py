from django.core.management import BaseCommand

from rate.models import CurrencyPair
from rate.services import GetRatesService


class Command(BaseCommand):
    help = 'Get rates of currencies.'

    def handle(self, *args, **options):
        self.stdout.write('Starting getting rates.')
        currency_pairs = CurrencyPair.objects.select_related(
            'base_currency', 'target_currency'
        )
        pair_list = [
            (
                pair.base_currency.code.lower(),
                pair.target_currency.code.lower()
            ) for pair in currency_pairs
        ]

        currency_service = GetRatesService(pair_list)
        currency_service.process()
        self.stdout.write('Get rates command has been finished.')
