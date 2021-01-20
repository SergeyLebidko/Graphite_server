from django.contrib import admin

from .models import Account, Token


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['login', 'username']
    list_display_links = ['login', 'username']
    search_fields = ['login', 'username']


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['account', 'token']
    list_display_links = ['account', 'token']
    search_fields = ['account']
