from celery import shared_task
from django.core.management import call_command


@shared_task
def update_currencies():
    # ToDo add celery logger
    print('Update currencies task started.')
    call_command('updatecurrencies')


@shared_task
def get_rates():
    # ToDo add celery logger
    print('Get rates task started.')
    call_command('getrates')
