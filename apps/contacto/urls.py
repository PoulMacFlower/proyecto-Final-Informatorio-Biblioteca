from django.urls import path
from .views import *

app_name = 'contacts'

urlpatterns = [
    path('Contact/', ContactView.as_view(), name = 'contact'),
]
