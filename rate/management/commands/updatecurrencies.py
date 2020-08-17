from django.core.management import BaseCommand

from rate.services import UpdateCurrenciesService


class Command(BaseCommand):
    help = 'Update list of currencies.'

    def handle(self, *args, **options):
        self.stdout.write('Starting updating currencies.')
        currency_servise = UpdateCurrenciesService()
        currency_servise.process()
        self.stdout.write('Updating currencies has been finished.')
