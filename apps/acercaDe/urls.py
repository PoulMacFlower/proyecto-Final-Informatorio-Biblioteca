from django.urls import path
from .views import *


app_name="About"

urlpatterns = [
    path('about/', AllAboutView.as_view(), name="about"),
]