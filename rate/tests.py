from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rate.models import Currency, CurrencyPair, Rate


class GetRatesViewTestCase(TestCase):
    def setUp(self) -> None:
        btc = Currency.objects.create(
            code='BTC',
            name='Bitcoine'
        )
        usd = Currency.objects.create(
            code='USD',
            name='USD'
        )
        uah = Currency.objects.create(
            code='UAH',
            name='Hryvna'
        )
        pair_1 = CurrencyPair.objects.create(
            base_currency=btc,
            target_currency=usd
        )
        pair_2 = CurrencyPair.objects.create(
            base_currency=usd,
            target_currency=uah
        )
        current_timestamp = timezone.now().timestamp()

        for i in range(13):
            Rate.objects.create(
                currency_pair=pair_1,
                price=Decimal(5 + i),
                timestamp=current_timestamp - i * 10
            )
            Rate.objects.create(
                currency_pair=pair_2,
                price=Decimal(30 - i),
                timestamp=current_timestamp - i * 10
            )

    def test_avg_latest_rates(self):
        response = self.client.get(reverse('rates'))
        self.assertEqual(response.status_code, 200)
        currency_pairs = response.context_data.get('currency_pairs')
        self.assertEqual(currency_pairs.count(), 2)

        pair_1 = currency_pairs.first()
        self.assertEqual(pair_1.base_currency.code, 'BTC')
        self.assertEqual(pair_1.target_currency.code, 'USD')
        self.assertEqual(pair_1.avg_price, 7.5)
        self.assertEqual(pair_1.get_latest_rate().price, 5)

        pair_2 = currency_pairs.last()
        self.assertEqual(pair_2.base_currency.code, 'USD')
        self.assertEqual(pair_2.target_currency.code, 'UAH')
        self.assertEqual(pair_2.avg_price, 27.5)
        self.assertEqual(pair_2.get_latest_rate().price, 30)
