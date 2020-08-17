from django.db import models
from django.utils.translation import gettext as _


class Currency(models.Model):
    code = models.CharField(
        _('Code'),
        max_length=10,
        unique=True,
        db_index=True
    )
    name = models.CharField(_('Name'), max_length=50)
    is_active = models.BooleanField(_('Is active'), default=False)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f'{self.code}({self.name})'


class CurrencyPair(models.Model):
    base_currency = models.ForeignKey(
        'Currency',
        verbose_name=_('Base currency'),
        related_name='base_currencies',
        on_delete=models.PROTECT,
    )
    target_currency = models.ForeignKey(
        'Currency',
        verbose_name=_('Target currency'),
        related_name='target_currencies',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f'{self.base_currency.name}-{self.target_currency.name}'

    def get_latest_rate(self):
        return self.rates.order_by('timestamp').last()


class Rate(models.Model):
    currency_pair = models.ForeignKey(
        'CurrencyPair',
        verbose_name=_('Currency Pair'),
        related_name='rates',
        on_delete=models.PROTECT
    )
    price = models.DecimalField(_('Price'), max_digits=20, decimal_places=10)
    timestamp = models.PositiveIntegerField(_('Unix Timestamp'), db_index=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.currency_pair.base_currency.name}-' \
               f'{self.currency_pair.target_currency.name} {self.price}'
