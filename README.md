# Graphite_server

Это серверная часть приложения Graphite. Более подробно о нем я рассказываю [в репозитории клиентской части](https://github.com/SergeyLebidko/graphite_client/blob/master/README.md). Здесь я ограничусь кратким описанием особенностей серверной части.

Серверная часть написана на Django. Для обработки запросов к api использован Django Rest Framework. 

Для обработки CORS я применил пакет django-cors-headers.
В файл settings.py помимо стандартных для django настроек также добавлены и настройки для CORS, требуемые этим пакетом:
```python
CORS_ORIGIN_WHITELIST = ['http://localhost:3000', 'http://127.0.0.1:3000', 'http://127.0.0.1', 'http://localhost']
```

Также в проекте я не использую стандартную систему работы с пользователями, предлагаемую Django (за исключением, конечно, создания суперпользователя для доступа к админке). 
Для хранения сведений о клиентах я написал свою модель - Account и дополнительную модель - Token - для отслеживания пользовательских сессий.
Работает механизм довольно просто: при регистрации нового пользователя или при выполнении входа ранее уже зарегистрированного генерируется новый токен, который отправлется браузеру пользователя. Браузер сохраняет токен в local storage и в дальнейшем использует его для выполнения запросов к api, требующих обязательной авторизации. При выполнении выхода из аккаунта (через соответствующих хук) текущий токен удаляется. Также предусмотрен хук для выхода одновременно на всех устройствах, на которых был до этого залогинен пользователь (хук для этого производит удаление всех токенов, связанных с данным пользователем в результате чего токены, сохраненные на устройствах станут недействительными и выполоняемые с их помощью запросы будут отклняться со статусом 403 Forbidden).

В файле settings.py предусмотрена настройка для установки длины токена:
```python
ACCOUNT_TOKEN_SIZE = 32
```

Аутентификация пользователя по токену производится автоматически с помощью простой middleware-функции, которая просматривает заголовок Authorization в запросе, извлекает из него токен и ищет в БД ассоцированного с токеном пользователя. Если пользователь найден, то в объекте запроса (request) создается поле account со ссылкой на соответствующего пользователя.
