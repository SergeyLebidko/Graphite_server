from django.contrib import admin

from .models import Account, Token, Post, Comment, PostLike, CommentLike


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
    list_display = ['title', 'account', 'dt_created']
    list_display_links = ['title']
    search_fields = ['account']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['short_comment_text', 'account']
    list_display_links = ['short_comment_text']
    search_fields = ['account']

    @staticmethod
    def short_comment_text(comment):
        return str(comment)


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'account']
    list_display_links = ['post', 'account']
    search_fields = ['post', 'account']


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['comment', 'account']
    list_display_links = ['comment', 'account']
    search_fields = ['comment', 'account']
