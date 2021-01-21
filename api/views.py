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
    requested_login = request.data.get('login', '')
    requested_password = to_hash(request.data.get('password', ''))

    account = Account.objects.filter(login=requested_login, password=requested_password).first()
    if not account:
        return Response({'error': 'Учетные данные не верны'}, status=status.HTTP_403_FORBIDDEN)

    token = create_random_string(settings.ACCOUNT_TOKEN_SIZE)
    Token.objects.create(token=token, account=account)

    return Response({'token': token}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PATCH'])
def accounts(request):
    if request.method in ['GET', 'PATCH'] and not request.account:
        return Response(status=status.HTTP_403_FORBIDDEN)

    # Аккаунт извлекается при получении запроса в middleware. Если его удалось получить - он уже будет в запросе
    if request.method == 'GET':
        serializer = AccountSerializer(request.account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
    if request.method == 'PATCH':
        serializer = AccountSerializer(data=request.data, instance=request.account)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
