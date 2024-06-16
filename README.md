<p align="center">
  <a href='' target='_blank'><img src='' height="auto" width="100%" style="border-radius:50%"></a>
</p>

# SeedVideo

## Описание проекта:
Платформа «SeedVideo» демонстрирует работу поисковой системы видео, направленной на извлечение данных из видео с целью индексации и поиска по этим данным.

## Возможности проекта:
Платформа позволяет пользователям загружать видео для индексации, а так же осуществлять поиск по ранее проиндексированным данным. 
Демонстрация работы компонентов индексации и поиска по индексированным данным. А так же фронтэнд часть для демонстрации работы этой системы с возможностью поиска видео, включая систему исправления опечаток и автодополнения при поиске видео.


## ЛИДЕРЫ ЦИФРОВОЙ ТРАНСФОРМАЦИИ 2024
## Задача: Сервис текстового поиска по медиаконтенту
 
### Команда Команда Простите, у нас вдохновение \ 2024.

![alt text](https://downloader.disk.yandex.ru/preview/d3cd19e7e42b524db4e96bcfde483a307110c35cffdd09fa675b30cb9a84eb68/666ebcae/w233wAFTgbikELyR3CxY71PRTKlIa7X2yT2RGzDs90xxvkzFlOweW2LiAct6uhwOWW0YOGNJ8RazrvxTAYLbeg%3D%3D?uid=0&filename=photo_2024-06-16_10-21-04.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2048x2048?raw=true)

### Суть проекта:
Платформа «Коммунальный Экспер» агрегирует данные об объектах, инцидентах и ремонтных работах из различных источников, связывает их и обрабатвыает с целью рекомендаций по будущим работам для предотвращения или более быстрого реагирования на инциденты.

### Описание архитектуры:

В нашем решении использована гибридная архитектура, позволяющая гибко извлекать необходимые данные из на нескольких уровнях: из произносимой речи на видео, из фоновой звуковой дорожки, из происходящего на видео, из пользовательского описания видео. Совокупность этих данных у нас векторизуется, и с помощью поиска по векторной базе мы предоставляем ТОП самых подходящих под описание запроса видео. Более того наша архитектура позволяет конфигурировать веса важности вышеописанных данных и использовать LLM с помощью RAG (контекстные запросы) чтобы находить видео еще на более глубоком уровне.
Мы извлекаем из видео 4 вида модальностей: субтитры, звуковую дорожку, описание содержимого видео, пользовательское описание. Описание содержимого мы извлекаем из n уникальных ключевых фреймов (кадров видео).

### Описание основных алгоритмов и моделей машинного обучения:
-    Алгоритмы хэширования для определения уникальности фреймов
-    Мультимодальная языковая модель
-    Алгоритмы автокомплита и исправленя ошибок по близости расстояния.
-    Алгоритмы векторизации
-    RAG.

### Архитектура сервиса:
![alt text](https://downloader.disk.yandex.ru/preview/b23b898db462b15b909cb1f69e498979a9e4ffb65585702da39972d1e921634d/666ebac9/E4pdVgGnyqTWUEhU2Ydoj9ausEqL93hVBN9G-F6JPu0uK6NCQDVakH8-CyjIgQaDZhaafH87wrF6yMhVW2x_6Q%3D%3D?uid=0&filename=arch.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=2048x2048?raw=true)

### Как мы обрабатываем видео:
В нашем решении использована гибридная архитектура, позволяющая гибко настраивать и извлекать необходимые данные из видео на нескольких уровнях: из произносимой речи на видео, из фоновой звуковой дорожки, из происходящего на видео, из пользовательского описания видео. Совокупность этих данных мы векторизуем, и с помощью поиска по векторной базе мы предоставляем ТОП самых подходящих под описание запроса видео. Более того наша архитектура позволяет конфигурировать веса важности вышеописанных данных и использовать LLM с помощью RAG (контекстные запросы) чтобы находить видео еще на более глубоком уровне.


## Возможности сервиса:
- Поиск по проиндексированной базе пользователя
- Индексация новых видео происходит практически реалтайм и данные попадают в базу
- Поиск по содержимому видео 
- Поиск по произнесённой речи в виде
- Поиск по описанию видео
- Поиск по тегам
- Интерпретация результатов выдачи
- Система скоринга при поисковой выдаче
- Система весов для тонкой настройки поиска\содание гибридной системы поика
- Быстрый отклик при поисковом запросе
- Исправление ошибок при наборе поискового запроса
- Система автодополнения запроса популярными запросами при наборе поискового запроса

Интерфейс. 

Основная часть интерфейса - это поисковая строка. Поисковая строка являестя интеллектуальной, позволяет предложить варианты на начально введенный запрос пользователя.
А таr же позволяют пользователю нивелировать не верно введённый запрос, предугадывая и исправляя его.
Еще одним приимуществом нашего поисковика являеся система весов, котораяпозволяет гибко настраивать качество поисковой выдачи в зависимости от настройки весов на различные модальности:

По видео - это основная фишка сервиса, в данной модальности хранятся описанные (визуальной языковой моделью) сцены на видео, другими словами интерпретация происходящего на видео (с помощью комбинации описаний нескольких уникальных фреймов).
По аудио - наша система умеет разделять* звуковую дорожку и извлекать отдельно речь и фоновую музыку\звуки. Благодаря этому мы можем качественно транскрибировать речь и перенести её в модальность.
* - благодаря этому в будущем можно векторизовать звуки и искать видео по загруженным трекам\звукам.
По тексту - по пользовательскому описанию видео.
По тегам - по введённым пользователем  тегам к видео.
Система позволяет интерпретировать результаты своего поиска и обосновывать свой выбор:

Каждому видео присваивается вероятность уверенности поисковика в принадлежности данного видео к поисковому запросу.
К тому же модель показывает на основе какой из модальностей был сделан вывод о принадлежности видео.
Мы пошли дальше и для большей интерпретируемости и продемонстрировали участки данных из модальностей, по которым система делает вывод:
В данном случае мы можем видеть разделённые фрейм и интерпретацию происходящего в них. Снизу модель обосновывает причину, в данном видео она услышала в произносимом автором видео слове Dota 
Дальнейшее совершенствование алгоритма позволяет добавить эвристику в динамический выбор модальностей и тем самым значительно ускорить время отклика при поиске.

## Преимущества нашего решения
Мы используем извлечение уникальных кадров, которые описываем с помощью мультимодальной языковой модели, чтобы понять что происходит на видео, даже если в нем нет описания, тегов и не произносится речь и нет фоновых звуков. Гибкость системы позволяет управлять количеством уникальных фреймов и порогом уникальности, размером окна ответа LLM, использовать разные модальности. Векторная база позволяет оптимизировать хранение проиндексированных данных и ускорять по ним поиск.
Мы подошли к вопросу извлечения данных для поиска основательно и используем самый глубокий из возможных подходов, который даёт глубокое понимание о происходящем на видео и позволяет его найти, даже если по нему нет информации от пользователя. Мы учли баланс между скоростью индексирования и скоростью поиска.


## Описание инструментов:
-    На беке Python, FastAPI, Celery, ChromaDB for servers
-    На фронте ReactJS, Consta.design

## Скорость работы:
-    Скорость индексации ~3-5 секунд на видео до 1 минуты в одном потоке
-    Скорость поиска ~470 мс на топ 10 видео

## Сложности при обработке данных:
- Видео файлы разной длины, поиск наилучего числа фреймов? извлечение уникальных фреймов определяется с помощью хэширования и вычисления дистанции в различиях
- В видео загруженных пользователем может вообще не быть описания и тегов
- Языковые модели плохо работают с русским языком
- Речь в видео не всегда можно извлечь качественно
- Индексация требует ГПУ вычислительных ресурсов

## API сервис:
Для работы с API сервисом можно использовать логины указанные выше. 
Вся документация по работе с сервисом указана в swagger по адресу:
 https://api.seedvideo.ru/docs
 пример опенапи: https://api.seedvideo.ru/openapi.json

![alt text](https://downloader.disk.yandex.ru/preview/10eca6396eb49d29a79b759327ee14a381f000f962955fdc23daa45c04244202/666ebb42/4_fohzMeE08ss7-VLzC44ARTceId5Jv37KI28vJzYOHQOIGpau6uVhLyztHx3t5SAm43pOz7uyDA_1vz5k4mfw%3D%3D?uid=0&filename=Firefox_Screenshot_2024-06-16T06-15-08.282Z.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=2048x2048?raw=true)

## Установка 

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

Для установки серверной части вам необходимо использовать Docker версии не ниже 20. Инструкцию по установке можете найти [здесь](https://docs.docker.com/engine/install/)
Далее вам следует заполнить файл переменных окружений. Например, следующим образом:

- git clone  https://github.com/ShakurovR/vsm
- cd livecity
- docker compose –f docker-compose.local.yml build —no-cache —pull
- docker compose –f docker-compose.local.yml up –d

Также для разворачивания только API сервиса можно использовать файл docker-compose.back.yml



## Полезные ссылки
- Веб сервис: [https://seedvideo.ru](https://seedvideo.ru)
- API сервис: [http://api.seedvideo.ru](http://api.seedvideo.ru)
- Документация API сервиса: [https://api.seedvideo.ru/docs](https://api.seedvideo.ru/docs)
- Github: [https://github.com/ShakurovR/vsm/tree/main](https://github.com/ShakurovR/vsm/tree/main)

## Стек используемых технологий и библиотек:
- Python/Pandas/regex
- FastAPI
- Sbercloud IaaS/PaaS Infrastructure
- Docker
- React js \ reduct
- ChromaDB
- OpenCV
- Nginx
- Postgresql
- LLama.cpp server





## Скринкаст

## Использованный стек

## Описание команды и контакты
