from django.urls import path
from project.views import get_params_view

urlpatterns = [
    path('', get_params_view, name='get_params_view'),
]
