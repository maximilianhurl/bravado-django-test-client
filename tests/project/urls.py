from django.urls import path

from project.views import get_params_view, cats_list, cat_update

urlpatterns = [
    path('', get_params_view, name='get_params_view'),
    path('cats/', cats_list, name='cats_list'),
    path('cats/<cat_name>/', cat_update, name='cat_update'),
]
