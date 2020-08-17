from django.urls import path

from . views import registration


app_name = 'registration'
urlpatterns = [
    path('', registration, name='registration'),
]
