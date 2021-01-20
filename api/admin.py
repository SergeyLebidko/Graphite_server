from django.contrib import admin

from .models import Account, Token, Post, Comment


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


class CommentAdmin(admin.ModelAdmin):
    list_display = ['short_comment_text', 'account']
    list_display_links = ['short_comment_text']
    search_fields = ['account']

    @staticmethod
    def short_comment_text(comment):
        return str(comment)
