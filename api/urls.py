from django.urls import path

from .views import gender_list, login, logout, register_account, check_account

app_name = 'api'

urlpatterns = [
    path('gender_list/', gender_list, name='gender_list'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register_account/', register_account, name='register_account'),
    path('check_account/', check_account, name='check_account')
]
