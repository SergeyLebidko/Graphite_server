from django.urls import path

from .views import gender_list, login, logout, logout_all_devices, register_account, check_account, \
    update_account

app_name = 'api'

urlpatterns = [
    path('gender_list/', gender_list, name='gender_list'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('logout_all_devices/', logout_all_devices, name='logout_all_devices'),
    path('register_account/', register_account, name='register_account'),
    path('check_account/', check_account, name='check_account'),
    path('update_account/', update_account, name='update_account')
]
