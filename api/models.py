from django.db import models


class AutoDateModel(models.Model):
    dt_created = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Account(AutoDateModel):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_LIST = (
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    )

    login = models.CharField(max_length=1000, verbose_name='Логин')
    password = models.CharField(max_length=1000, verbose_name='Пароль')
    username = models.CharField(max_length=1000, verbose_name='Имя пользователя')
    birth_date = models.DateField(verbose_name='Дата рождения')
    gender = models.CharField(max_length=1, verbose_name='Пол', choices=GENDER_LIST)
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
    account = models.ForeignKey(Account, verbose_name='Аккаунт', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
