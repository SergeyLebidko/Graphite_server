from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from api.models import Token
import time


def account_middleware(next_view):
    def middleware(request):
        token = request.headers.get('authorization')
        try:
            request.account = Token.objects.filter(token=token).first().account
            request.token = token
        except AttributeError:
            request.account = None
            request.token = None
        return next_view(request)

    return middleware


class LagMiddleware:

    def __init__(self, next_view):
        if not settings.DEBUG:
            raise MiddlewareNotUsed()
        self.next_view = next_view

    def __call__(self, *args, **kwargs):
        time.sleep(settings.LAG)
        return self.next_view(*args, **kwargs)
