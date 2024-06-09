<p align="center">
  <a href='' target='_blank'><img src='' height="auto" width="100%" style="border-radius:50%"></a>
</p>


# Название проекта

## Описание проекта:

## Возможности проекта:

## Запуск
Для установки серверной части вам необходимо использовать Docker версии не ниже 20. Инструкцию по установке можете найти [здесь](https://docs.docker.com/engine/install/)

Далее вам следует заполнить файл переменных окружений. Например, следующим образом:

***.env***
```
PROJECT_NAME=name
PGSQL_URL=postgresql://root:password@pgsql/name
PGSQL_USERNAME=root
PGSQL_PASSWORD=password
PGSQL_DATABASE=name
PGSQL_DATA=/data/
RABBITMQ_USERNAME=root
RABBITMQ_PASSWORD=password
CELERY_BROKER_URL=amqp://root:password@rabbitmq:5672//
CELERY_RESULT_BACKEND=redis://redis:6379/0
KEYCLOAK_ADMIN=root
KEYCLOAK_ADMIN_PASSWORD=password
API_BASE_URL=http://localhost:9000/
API_MEDIA_URL=http://localhost/files/
API_MEDIA_PATH=media
REACT_APP_API_URL=http://localhost:9000/
```

## Скринкаст

## Использованный стек

## Описание команды и контакты
