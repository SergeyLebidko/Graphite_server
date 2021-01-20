from django.contrib import admin

from .models import Account, Token, Post


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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'account']
    list_display_links = ['title']
    search_fields = ['account']
