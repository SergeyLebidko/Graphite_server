from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from utils import to_hash, create_random_string
from .models import Account, Token, Post
from .serializers import AccountSerializer, PostSerializer
from .permissions import HasAccountPermission, HasPostPermission


@api_view(['GET'])
def gender_list(request):
    return Response(dict(Account.GENDER_LIST), status=status.HTTP_200_OK)


@api_view(['POST'])
def register_account(request):
    """Создает новый аккаунт"""

    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """По переданным данным (логин/пароль) создает и возвращает новый токен доступа"""

    requested_login = request.data.get('login')
    requested_password = to_hash(request.data.get('password'))
    account = Account.objects.filter(login=requested_login, password=requested_password).first()
    if not account:
        return Response({'error': 'Учетные данные не верны'}, status=status.HTTP_400_BAD_REQUEST)
    token = create_random_string(settings.ACCOUNT_TOKEN_SIZE)
    Token.objects.create(token=token, account=account)
    return Response({'token': token}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([HasAccountPermission])
def logout(request):
    """Удаляет переданный токен (тем самым осуществляя выход из аккаунта на устройстве с данным токеном)"""

    Token.objects.filter(token=request.token).first().delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([HasAccountPermission])
def logout_all_devices(request):
    """Удаляет все токены пользователя (тем самым осуществляя выход на всех устройствах с сохраненными токенами)"""

    Token.objects.filter(account=request.account).delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([HasAccountPermission])
def check_account(request):
    """Возвращает данные аккаунта по переданному токену"""

    serializer = AccountSerializer(request.account)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([HasAccountPermission])
def update_account(request):
    """Изменяет у аккаунта любые поля, кроме лоигина и пароля (для их смены предусмотрены отдельные хуки)"""

    serializer = AccountSerializer(request.account, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([HasAccountPermission])
def change_login(request):
    """Изменяет логин аккаунта. Для подтверждения операции требует пароль"""

    account = request.account
    requested_login = request.data.get('login')
    requested_password = to_hash(request.data.get('password'))
    if requested_password != account.password:
        return Response({'error': 'Пароль не верен'}, status=status.HTTP_400_BAD_REQUEST)

    login_exists = Account.objects.filter(login=requested_login).exists()
    if login_exists:
        return Response({'error': 'Такой логин уже занят'}, status=status.HTTP_400_BAD_REQUEST)

    account.login = requested_login
    account.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([HasAccountPermission])
def change_password(request):
    """Изменяет пароль аккаунта. Для подтверждения операции требует старый пароль"""

    account = request.account
    current_password = to_hash(request.data.get('password'))
    next_password = to_hash(request.data.get('next_password'))
    if current_password != account.password:
        return Response({'error': 'Пароль не верен'}, status=status.HTTP_400_BAD_REQUEST)

    account.password = next_password
    account.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([HasAccountPermission])
def remove_account(request):
    """Удаляет аккаунт"""

    account = request.account
    requested_password = to_hash(request.data.get('password'))
    if requested_password != account.password:
        return Response({'error': 'Пароль не верен'}, status=status.HTTP_400_BAD_REQUEST)

    account.delete()
    return Response(status=status.HTTP_200_OK)


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [HasPostPermission]

    def get_queryset(self):
        queryset = Post.objects.all()
        return queryset
