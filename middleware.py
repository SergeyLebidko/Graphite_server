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
