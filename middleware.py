from django.conf import settings
from api.models import Token


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


def cors_middleware(next_view):
    def middleware(request):
        response = next_view(request)
        response['Access-Control-Allow-Origin'] = settings.CORS_HOST
        return response

    return middleware
