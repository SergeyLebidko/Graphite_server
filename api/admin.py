from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['login', 'username']
    list_display_links = ['login', 'username']
    search_fields = ['login', 'username']
