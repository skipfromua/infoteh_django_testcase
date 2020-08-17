from django.urls import path

from .views import main_page, create_and_publish_message


app_name = 'message_publisher'
urlpatterns = [
    path('', main_page, name='main'),
    path('create', create_and_publish_message, name='create')
]
