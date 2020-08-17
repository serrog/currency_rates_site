import asyncio
from decimal import Decimal

import aiohttp
from aiohttp import ClientSession
from asgiref.sync import sync_to_async

from rate.models import Currency, Rate, CurrencyPair


class BaseFetchRatesService:
    """
    base Service for fetching and saving in the DB rates for currencies
    """
    _api_endpoint = None

    def _prepare_urls(self) -> list:
        raise NotImplementedError

    @sync_to_async
    def _update_currencies(self, data: dict) -> None:
        raise NotImplementedError

    def process(self) -> None:
        async def fetch_url(url: str, session: ClientSession) -> dict:
            try:
                resp = await session.request(
                    method="GET",
                    url=url,
                    # it's a hack
                    # get rates endpoint does't work without user agent
                    # ToDo check what fake user agent could be added
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Masc '
                                      'OS X 10_15_6) AppleWebKit/605.1.15 '
                                      '(KHTML, like Gecko) Version/13.1.2 '
                                      'Safari/605.1.15'
                    }
                )
                resp.raise_for_status()
                data = await resp.json()
            except aiohttp.ClientError as e:
                # ToDo add error log
                pass
            else:
                return data

        async def fetch_and_update(url: str, session: ClientSession) -> None:
            data = await fetch_url(url, session)
            await self._update_currencies(data)

        async def bulk_fetch(url_list: list) -> None:
            tasks = []
            async with aiohttp.ClientSession() as session:
                for url in url_list:
                    tasks.append(fetch_and_update(url, session))
                await asyncio.gather(*tasks)

        url_list = self._prepare_urls()
        result = asyncio.run(bulk_fetch(url_list))
        return result


class UpdateCurrenciesService(BaseFetchRatesService):
    """
    Service for fetching and updating currencies in the DB
    """
    _api_endpoint = 'https://www.cryptonator.com/api/currencies'

    def _prepare_urls(self) -> list:
        return [self._api_endpoint]

    @sync_to_async
    def _update_currencies(self, data: dict) -> None:
        for currency in data.get('rows', []):
            Currency.objects.update_or_create(
                code=currency.get('code'),
                defaults={'name': currency.get('name')}
            )


class GetRatesService(BaseFetchRatesService):
    """
    Service for fetching and saving in the DB rates for currencies
    currency_pairs: list of tuples (base, target),
        example [('BTC', 'USD'), ('USD', 'UAH')]
    """
    _api_endpoint = 'https://api.cryptonator.com/api/ticker/'

    def __init__(self, currency_pairs: list):
        self.currency_pairs = currency_pairs

    def _prepare_urls(self) -> list:
        url_list = [
            self._api_endpoint + f'{c[0].lower()}-{c[1].lower()}'
            for c in self.currency_pairs
        ]
        return url_list

    @sync_to_async
    def _update_currencies(self, data: dict) -> None:
        ticker = data.get('ticker', {})
        if data.get('success'):
            base_currency = Currency.objects.get(code=ticker.get('base'))
            target_currency = Currency.objects.get(code=ticker.get('target'))
            currency_pair = CurrencyPair.objects.filter(
                base_currency=base_currency,
                target_currency=target_currency
            ).first()
            if currency_pair:
                Rate.objects.create(
                    currency_pair=currency_pair,
                    price=Decimal(ticker.get('price')),
                    timestamp=data.get('timestamp')
                )
        else:
            error = ticker.get('error')
            # ToDo log error
