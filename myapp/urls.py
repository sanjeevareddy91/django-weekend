from django.urls import path
from .views import hello,register_data,data_list, single_data, update_data,delete_data

urlpatterns = [
    path('hello',hello),
    path('register',register_data,name="register_data"),
    path('list',data_list,name="data_list"),
    path('single_data/<name>',single_data,name="single_data"),
    path('update_data/<name>',update_data,name="update_data"),
    path('delete_data/<name>',delete_data,name="delete_data"),
]
