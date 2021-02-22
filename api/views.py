from django.conf import settings
from django.db.models import Sum, Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status

from utils import to_hash, create_random_string
from .models import Account, Token, Post, PostLike, Comment, CommentLike
from .serializers import AccountSerializer, PostSerializer, CommentSerializer
from .permissions import HasAccountPermission, HasPostPermission, HasCommentPermission
from .pagination import CustomPagination
from .full_text_search import search


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


@api_view(['GET'])
def account_stat(request):
    """Возвращает статистику аккаунта: количество постов, лайков, комментариев и просмотров постов"""

    account_id = request.query_params.get('account')
    account = Account.objects.get(pk=account_id)
    posts = Post.objects.filter(account=account)

    post_count = posts.count()
    total_views_count = posts.aggregate(cnt=Sum('views_count'))['cnt']
    if total_views_count is None:
        total_views_count = 0

    like_count = PostLike.objects.filter(post__account=account).count()
    comment_count = Comment.objects.filter(post__account=account).count()

    return Response(
        data={
            'post_count': post_count,
            'like_count': like_count,
            'comment_count': comment_count,
            'total_views_count': total_views_count
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def post_stat(request):
    """Возвращает статистику поста: количество просмотров, лайков и комментариев"""

    post_id = request.query_params.get('post')
    post = Post.objects.get(pk=post_id)

    like_count = PostLike.objects.filter(post=post).count()
    comment_count = Comment.objects.filter(post=post).count()
    views_count = post.views_count

    return Response(
        data={
            'like_count': like_count,
            'comment_count': comment_count,
            'views_count': views_count
        },
        status=status.HTTP_200_OK
    )


class AccountViewSet(ReadOnlyModelViewSet):
    serializer_class = AccountSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Account.objects.all().order_by('-dt_created')

        order = self.request.query_params.get('order')
        if order == 'views':
            queryset = queryset.annotate(cnt=Sum('post__views_count')).order_by('-cnt')
        if order == 'likes':
            queryset = queryset.annotate(cnt=Count('post__postlike')).order_by('-cnt')
        if order == 'comments':
            queryset = queryset.annotate(cnt=Count('post__comment')).order_by('-cnt')

        q = self.request.query_params.get('q')
        if q:
            return search(queryset, q, 'account')

        return queryset


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [HasPostPermission]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Post.objects.select_related('account').all()
        account = self.request.query_params.get('account')
        if account:
            queryset = queryset.filter(account=account)

        order = self.request.query_params.get('order')
        if order == 'views':
            queryset = queryset.order_by('-views_count')
        if order == 'likes':
            queryset = queryset.annotate(cnt=Count('postlike')).order_by('-cnt')
        if order == 'comments':
            queryset = queryset.annotate(cnt=Count('comment')).order_by('-cnt')

        q = self.request.query_params.get('q')
        if q:
            return search(queryset, q, 'post')

        return queryset

    def retrieve(self, request, *args, **kwargs):
        account = request.account
        post = self.get_object()

        if not account or account.pk != post.account.pk:
            post.views_count += 1
            post.save()
        result = ModelViewSet.retrieve(self, request, *args, **kwargs)
        return result


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [HasCommentPermission]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-dt_created')

        post = self.request.query_params.get('post')
        if post:
            queryset = queryset.filter(post_id=post)

        return queryset


@api_view(['GET', 'POST'])
@permission_classes([HasAccountPermission])
def post_like(request):
    return _like(request, 'post')


@api_view(['GET', 'POST'])
@permission_classes([HasAccountPermission])
def comment_like(request):
    return _like(request, 'comment')


def _like(request, _type):
    account = request.account
    model = {'post': PostLike, 'comment': CommentLike}[_type]
    param = request.query_params.get(_type) if request.method == 'GET' else request.data.get(_type)

    kwargs = {
        'post': {'post_id': param, 'account': account},
        'comment': {'comment_id': param, 'account': account}
    }[_type]

    if request.method == 'GET':
        exists = model.objects.filter(**kwargs).exists()
        return Response({'exists': exists}, status=status.HTTP_200_OK)

    like, create_flag = model.objects.get_or_create(**kwargs)
    if not create_flag:
        like.delete()

    return Response({'exists': create_flag}, status=status.HTTP_200_OK)
