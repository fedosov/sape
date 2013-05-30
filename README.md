# django-sape

## Настройка

`settings.py`

```
INSTALLED_APPS = \
(
    ...
    'sape',
    ... 
)
```

```
SAPE_DOMAIN = 'example.com'
SAPE_USER = 'sape_username'
SAPE_CHARSET = 'utf8'
SAPE_DIR = '/tmp/sape_cache/'
```

## Запрос ссылок (обновление кеша)

`./manage.py sape fetch`