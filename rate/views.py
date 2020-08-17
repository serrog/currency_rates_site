from django.db.models import Avg, Q
from django.views.generic.edit import FormView
from django.utils import timezone

from rate.forms import CurrencyPairForm
from rate.models import CurrencyPair


class RatesView(FormView):
    template_name = 'rates.html'
    form_class = CurrencyPairForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        current_timestamp = timezone.now().timestamp()
        currency_pairs = CurrencyPair.objects.select_related(
            'base_currency', 'target_currency'
        ).annotate(
            avg_price=Avg(
                'rates__price', filter=Q(
                    rates__timestamp__gte=current_timestamp - 60
                )
            )
        )
        ctx['currency_pairs'] = currency_pairs
        return ctx

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
