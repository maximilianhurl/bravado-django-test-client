from django.urls import path
from project.views import index

urlpatterns = [
    path('', index, name='index'),
]
