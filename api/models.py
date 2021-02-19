from django.db import models


class AutoDateModel(models.Model):
    dt_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Account(AutoDateModel):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_LIST = (
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    )

    username = models.CharField(
        max_length=1000,
        verbose_name='Имя пользователя',
        unique=True,
        error_messages={'unique': 'Аккаунт с таким именем пользователя уже существует'}
    )
    login = models.CharField(
        max_length=1000,
        verbose_name='Логин',
        unique=True,
        error_messages={'unique': 'Аккаунт с таким логином уже существует'}
    )
    password = models.CharField(max_length=1000, verbose_name='Пароль')
    birth_date = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    gender = models.CharField(max_length=1, verbose_name='Пол', choices=GENDER_LIST, null=True, blank=True)
    description = models.TextField(verbose_name='О себе', blank=True, default='')
    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatars', null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
        ordering = ['username']


class Token(models.Model):
    token = models.CharField(max_length=32, verbose_name='Токен пользователя')
    account = models.ForeignKey(Account, verbose_name='Аккаунт', on_delete=models.CASCADE)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = 'Токен пользователя'
        verbose_name_plural = 'Токены пользователей'


class Post(AutoDateModel):
    title = models.CharField(max_length=1000, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    views_count = models.IntegerField(verbose_name='Количество просмотров', default=0)
    account = models.ForeignKey(Account, verbose_name='Аккаунт', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-dt_created']


class Comment(AutoDateModel):
    text = models.TextField(verbose_name='Текст')
    account = models.ForeignKey(Account, verbose_name='Аккаунт', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name='Пост', on_delete=models.CASCADE)

    def __str__(self):
        if len(self.text) < 50:
            return self.text
        return self.text[:50] + '...'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Лайк под постом')
    account = models.ForeignKey(Account, verbose_name='Аккаунт', on_delete=models.CASCADE)

    def __str__(self):
        return f'Лайк пользователя {self.account} под постом {self.post}'

    class Meta:
        verbose_name = 'Лайк под постом'
        verbose_name_plural = 'Лайки под постами'
        unique_together = ['post', 'account']


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Лайк под комментарием')
    account = models.ForeignKey(Account, verbose_name='Аккаунт', on_delete=models.CASCADE)

    def __str__(self):
        return f'Лайк пользователя {self.account} под комментарием {self.comment}'

    class Meta:
        verbose_name = 'Лайк под комментарием'
        verbose_name_plural = 'Лайки под комментариями'
        unique_together = ['comment', 'account']
