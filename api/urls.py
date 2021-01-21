from django.urls import path

from .views import gender_list, login, accounts

app_name = 'api'

urlpatterns = [
    path('gender_list/', gender_list, name='gender_list'),
    path('login/', login, name='login'),
    path('accounts/', accounts, name='accounts')
]
