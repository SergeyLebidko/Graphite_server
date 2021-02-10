from django.urls import path

from rest_framework.routers import SimpleRouter

from .views import gender_list, login, logout, logout_all_devices, register_account, check_account, \
    update_account, change_login, change_password, remove_account, PostViewSet, account_stat

app_name = 'api'

urlpatterns = [
    path('gender_list/', gender_list, name='gender_list'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('logout_all_devices/', logout_all_devices, name='logout_all_devices'),
    path('register_account/', register_account, name='register_account'),
    path('check_account/', check_account, name='check_account'),
    path('update_account/', update_account, name='update_account'),
    path('change_login/', change_login, name='change_login'),
    path('change_password/', change_password, name='change_password'),
    path('remove_account/', remove_account, name='remove_account'),
    path('account_stat/', account_stat, name='account_stat')
]

router = SimpleRouter()
router.register('posts', PostViewSet, basename='post')
urlpatterns.extend(router.urls)
