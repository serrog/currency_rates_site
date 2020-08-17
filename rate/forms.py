from django.forms import ModelForm

from rate.models import CurrencyPair


class CurrencyPairForm(ModelForm):
    class Meta:
        model = CurrencyPair
        fields = ['base_currency', 'target_currency']
