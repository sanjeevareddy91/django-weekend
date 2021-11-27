from django.contrib.auth import logout
from django.urls import path
from .views import hello, login_user,register_data,data_list, single_data, update_data,delete_data,register_modelform,register_normalform,login_user,logout_user,forgot_password, verify_otp, confirm_password

urlpatterns = [
    path('hello',hello),
    path('register/',register_data,name="register_data"),
    path('list',data_list,name="data_list"),
    path('single_data/<name>',single_data,name="single_data"),
    path('update_data/<name>',update_data,name="update_data"),
    path('delete_data/<name>',delete_data,name="delete_data"),
    path('register_modelform',register_modelform,name="register_modelform"),
    path('register_normalform',register_normalform,name="register_normalform"),
    path('login/',login_user,name="login_user"),
    path('logout/',logout_user,name="logout_user"),
    path('forgot_password/',forgot_password,name='forgot_password'),
    path('verify_otp/<id>',verify_otp,name='verify_otp'),
    path('confirm_password/<id>',confirm_password,name='confirm_password'),
]
