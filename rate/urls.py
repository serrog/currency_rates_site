from django.urls import path

from rate.views import RatesView


urlpatterns = [
    path('', RatesView.as_view(), name='rates'),
]
