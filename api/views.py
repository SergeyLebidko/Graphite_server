from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from utils import to_hash, create_random_string
from .models import Account, Token
from .serializers import AccountSerializer


@api_view(['GET'])
def gender_list(request):
    return Response(dict(Account.GENDER_LIST), status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
    """По переданным данным (логин/пароль) создает и возвращает новый токен доступа"""

    requested_login = request.data.get('login', '')
    requested_password = to_hash(request.data.get('password', ''))
    account = Account.objects.filter(login=requested_login, password=requested_password).first()
    if not account:
        return Response({'error': 'Учетные данные не верны'}, status=status.HTTP_403_FORBIDDEN)
    token = create_random_string(settings.ACCOUNT_TOKEN_SIZE)
    Token.objects.create(token=token, account=account)
    return Response({'token': token}, status=status.HTTP_200_OK)


@api_view(['GET'])
def logout(request):
    """Удалает переданный токен (тем самым осуществляя выход из аккаунта на устройстве с данным токеном)"""

    token = Token.objects.filter(token=request.token).first()
    if token:
        token.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def register_account(request):
    """Создает новый аккаунт"""

    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_account(request):
    """Возвращает данные аккаунта по переданному токену"""

    if request.account:
        serializer = AccountSerializer(request.account)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)
