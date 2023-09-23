# Yacloud

С помощью этого сервиса пользователи могут сохранить различные типы файлов в интернете — документы, фотографии, другие данные.
Проект представляет собой **http-сервис**, который обрабатывает поступающие запросы.



## Технологии

Python 3.11, FastAPI, PostgreSQL, SQLAlchemy, asyncpg, uvicorn, Docker, JWT, git

## Возможности сервиса

<details>
<summary> Список эндпойнтов. </summary>

1. Статус активности связанных сервисов.

    <details>
    <summary> Описание изменений. </summary>

    ```
    GET /ping
    ```
    Получить информацию о времени доступа ко всем связанным сервисам, например, к БД, кэшам, примонтированным дискам и т.д.

    **Response**
    ```json
    {
        "db": 1.27,
        "cache": 1.89,
        ...
        "service-N": 0.56
    }
    ```
   </details>


2. Регистрация пользователя.

    <details>
    <summary> Описание изменений. </summary>

    ```
    POST /register
    ```
    Регистрация нового пользователя. Запрос принимает на вход логин и пароль для создания новой учетной записи.

    </details>


3. Авторизация пользователя.

    <details>
    <summary> Описание изменений. </summary>

    ```
    POST /auth
    ```
    Запрос принимает на вход логин и пароль учетной записи и возвращает авторизационный токен. Далее все запросы проверяют наличие токена в заголовках - `Authorization: Bearer <token>`

    </details>


4. Информация о загруженных файлах.

    <details>
    <summary> Описание изменений. </summary>

    ```
    GET /files/
    ```
    Вернуть информацию о ранее загруженных файлах. Доступно только авторизованному пользователю.

    **Response**
    ```json
    {
        "account_id": "AH4f99T0taONIb-OurWxbNQ6ywGRopQngc",
        "files": [
              {
                "id": "a19ad56c-d8c6-4376-b9bb-ea82f7f5a853",
                "name": "notes.txt",
                "created_ad": "2020-09-11T17:22:05Z",
                "path": "/homework/test-fodler/notes.txt",
                "size": 8512,
                "is_downloadable": true
              },
            ...
              {
                "id": "113c7ab9-2300-41c7-9519-91ecbc527de1",
                "name": "tree-picture.png",
                "created_ad": "2019-06-19T13:05:21Z",
                "path": "/homework/work-folder/environment/tree-picture.png",
                "size": 1945,
                "is_downloadable": true
              }
        ]
    }
    ```
    </details>


5. Загрузить файл в хранилище.

    <details>
    <summary> Описание изменений. </summary>

    ```
    POST /files/upload
    ```
    Метод загрузки файла в хранилище. Доступно только авторизованному пользователю.
    Для загрузки заполняется полный путь до файла, в который будет загружен/переписан загружаемый файл. Если нужные директории не существуют, то они создаются автоматически.
    Так же есть возможность указать только путь до директории. В этом случае имя создаваемого файла будет создано в соответствии с передаваемым именем файла.

    **Request**
    ```
    {
        "path": <full-path-to-file>||<path-to-folder>,
    }
    ```

    **Response**
    ```json
    {
        "id": "a19ad56c-d8c6-4376-b9bb-ea82f7f5a853",
        "name": "notes.txt",
        "created_ad": "2020-09-11T17:22:05Z",
        "path": "/homework/test-fodler/notes.txt",
        "size": 8512,
        "is_downloadable": true
    }
    ```
    </details>


6. Скачать загруженный файл.

    <details>
    <summary> Описание изменений. </summary>

    ```
    GET /files/download
    ```
    Скачивание ранее загруженного файла. Доступно только авторизованному пользователю.

    **Path parameters**
    ```
    /?path=<path-to-file>||<file-meta-id>
    ```
    Возможность скачивания есть как по переданному пути до файла, так и по идентификатору.
    </details>

</details>



<details>
<summary> Список эндпойнтов - планы по расширению приложения. </summary>


1. Добавление возможности скачивания в архиве.
   <details>

   <summary> Описание изменений. </summary>

    ```
    GET /files/download
    ```
    Path-параметр расширяется дополнительным параметром – `compression`. Доступно только авторизованному пользователю.

    Дополнительно в `path` можно указать как путь до директории, так и его **UUID**. При скачивании директории скачаются все файлы, находящиеся в ней.

    **Path parameters**
    ```
    /?path=[<path-to-file>||<file-meta-id>||<path-to-folder>||<folder-meta-id>] & compression"=[zip||tar||7z]
    ```
    </details>


2. Добавление информация об использовании пользователем дискового пространства.

    <details>
    <summary> Описание изменений. </summary>

    ```
    GET /user/status
    ```
    Вернуть информацию о статусе использования дискового пространства и ранее загруженных файлах. Доступно только авторизованному пользователю.

    **Response**
    ```json
    {
        "account_id": "taONIb-OurWxbNQ6ywGRopQngc",
        "info": {
            "root_folder_id": "19f25-3235641",
            "home_folder_id": "19f25-3235641"
        },
        "folders": [
            "root": {
                "allocated": "1000000",
                "used": "395870",
                "files": 89
            },
            "home": {
                "allocated": "1590",
                "used": "539",
                "files": 19
            },
            ...,
            "folder-188734": {
                "allocated": "300",
                "used": "79",
                "files": 2
          }
        ]
    }
    ```
    </details>


3. Добавление возможности поиска файлов по заданным параметрам.

    <details>
    <summary> Описание изменений. </summary>

    ```
    POST /files/search
    ```
    Вернуть информацию о загруженных файлах по заданным параметрам. Доступно только авторизованному пользователю.

    **Request**
    ```json
    {
        "options": {
            "path": <folder-id-to-search>,
            "extension": <file-extension>,
            "order_by": <field-to-order-search-result>,
            "limit": <max-number-of-results>
        },
        "query": "<any-text||regex>"
    }
    ```

    **Response**
    ```json
    {
        "mathes": [
              {
                "id": "113c7ab9-2300-41c7-9519-91ecbc527de1",
                "name": "tree-picture.png",
                "created_ad": "2019-06-19T13:05:21Z",
                "path": "/homework/work-folder/environment/tree-picture.png",
                "size": 1945,
                "is_downloadable": true
              },
            ...
        ]
    }
    ```
    </details>


4. Поддержка версионирования изменений файлов.

    <details>
    <summary> Описание изменений. </summary>

    ```
    POST /files/revisions
    ```
    Вернуть информацию об изменениях файла по заданным параметрам. Доступно только авторизованному пользователю.

    **Request**
    ```json
    {
        "path": <path-to-file>||<file-meta-id>,
        "limit": <max-number-of-results>
    }
    ```

    **Response**
    ```json
    {
        "revisions": [
              {
                "id": "b1863132-5db6-44fe-9d34-b944ab06ad81",
                "name": "presentation.pptx",
                "created_ad": "2020-09-11T17:22:05Z",
                "path": "/homework/learning/presentation.pptx",
                "size": 3496,
                "is_downloadable": true,
                "rev_id": "676ffc2a-a9a5-47f6-905e-99e024ca8ac8",
                "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "modified_at": "2020-09-21T05:13:49Z"
              },
            ...
        ]
    }
    ```
    </details>

</details>


## Локальный запуск проекта
1. Подготовьте окружение

* Установите Docker
* Установите docker-compose
* Перейдите в директорию проекта с файлом docker-compose.yaml (по умолчанию: корень проекта)

2. Создайте файл переменных среды 

Создайте в текущей папке файл .env со значениями переменных среды.

(см пример файла .env.example в корне проекта)


3. Соберите и запустите контейнеры Docker
```shell
# В корне проекта
make build
make up
```

Проект развернут! [Документация](http://localhost:8080/api/openapi) 


4. Дополнительные полезные команды
```shell
# В корне проекта
make stop         # Остановить контейнеры
make down         # Удалить контейнеры
make test         # Запустить тесты
make exec_backend # Получить доступ в контейнер бэкенда
```

## Авторы

[Илья Боюр](https://github.com/IlyaBoyur)