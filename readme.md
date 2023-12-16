# __Дипломный проект на тему:__  
# __Разработка новостного портала с использованием фреймворка Django__  
  
# Задача
Разработать сайт новостей с возможностью дальнейшего расширения

# Описание
__Новостной портал даёт возможность неавторизованным пользователям просматривать новости, комментарии к ним, страницу о сайте, контакты, проходить регистрацию.__ 

__Зарегистрированные и авторизованные пользователи могут оставлять комментарии, имеют доступ к своему профилю и возможность его редактирования__

__Пользователям, имеющие статус персоонала, доступна возможность добавления новых статей.__

__Интерфейс администратора предоставляет возможность редактирования содержания страницы о сайте, контактов, пользователей, категорий новостей, самих новостей и комментариев к ним__

## Инструменты: 
Python, Django, Git, Visual Studio Code

## Локальный запуск проекта

### 1 Создать виртуальное окружение

### 2 Установить зависимости

    pip install -r requirements.txt

### 3 Выполнить миграции

    python manage.py migrate    

### 4 Создать суперпользователя

    python manage.py createsuperuser

### Старт

    python manage.py runserver

# Развертывание проекта на сервере www.pythonanywhere.com
### 1 Внести изменения в файл settings.py
* выключить режим отладки
    ```
   DEBUG = False
    ```
* Добавить константы для повышения безопасности раюоты с сессиями и crf токенами
    ```
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    ```
* Внести изменения в переменную для работы с секретным ключом, хранящимся в переменных окружения
    ```
    import os
    ...
    SECRET_KEY = os.getenv('SECRET_KEY')
    ```
* Добавить адрес сайта в список доступных хостов
    ```
    ALLOWED_HOSTS = [   
    ...
    '<username>.pythonanywhere.com',
    ]
    ```
* Добавить константу для работы со статистическими файлами
    ```
    STATIC_ROOT = BASE_DIR / 'static/'
    ```

### 2 Настроить подключение к базе данных
* Открыть раздел базы данных на хосте, придумать пароль для доступа к БД, дождаться завершения инициализации БД. По умолчанию создается БД username$default. Кликнув по имени, открываем консоль MySQL и вводим команду для смены кодировки на  UTF-8:
    ```
    ALTER DATABASE username$default CHARACTER SET utf8 COLLATE utf8_general_ci;
    ```
* В файле settings.py настроить подключение к БД
    ```
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<your_username>$default',
        'USER': '<your_username>',
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': '<your_username>.mysql.pythonanywhere-services.com',
        'OPTIONS': {
            'init_command': "SET NAMES 'utf8mb4';SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            },
        }
    }
    ```

### 3 Клонировать репозиторий
Перейти на вкладку Dashboard и открыть Bash консоль 
Воспользоваться коммандой
```
git clone https://github.com/Kite343/Diploma.git
```

### 4 Настройка проекта на сервере
* в Bash консоли запустить команду на создание виртуального окружения
    ```
    mkvirtualenv --python=/usr/bin/python3.10 virtualenv
    ```
* Установить необходимые пакеты
    ```
    cd myproject
    pip install -r requirements.txt
    ```
* Создать веб-приложение

    на вкладке Dashboard выбрать пункт Web apps и
и нажать кнопку Add a new web app
  1.  Подтвердить доменное имя для бесплатного профиля кнопкой Next
  2.  Выбирать пункт Manual configuration (including virtualenvs)
  3.  Выбирать последнюю из доступных версий Python
  4.  Подтвердить выбор очередным нажатием Next

* Настройка веб-приложения

    1. На вкладке настроек веб-приложения найти раздел Virtualenv и указать путь до окружения
        ```
        /home/username/.virtualenvs/virtualenv
        ```
    2. Отредактировать wsgi файл, ссылка на который находится в разделе Code.
    Заменить его содержимое на:
        ```
        import os
        import sys

        from dotenv import load_dotenv

        project_folder = os.path.expanduser('~/news_project/city_newsproject')
        load_dotenv(os.path.join(project_folder, '.env'))

        path = '/home/<your_username>/news_project/city_newsproject'
        if path not in sys.path:
            sys.path.append(path)

        os.environ['DJANGO_SETTINGS_MODULE'] = 'city_newsproject.settings'

        # then:
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        ```

    3. Сохранить "секреты" в окружении: проверить, что мы находимся в той же директории, что указана в wsgi файле в для переменной project_folder и выполнить команды:
        ```
        echo "export SECRET_KEY=<secret_key>" >> .env
        echo "export MYSQL_PASSWORD=<db_password>" >> .env
        ```
    4. Настроить доступ к переменным
        ```
        echo 'set -a; source ~/myproject/.env; set +a' >> ~/.virtualenvs/virtualenv/bin/postactivate
        ```
    5. Выйти из консоли командой exit. На вкладке Web в разделе Virtualenv кликом по кнопке Start открываем консоль и применяем миграции к БД
        ```
        python manage.py migrate
        ```
    6. Создать суперпользователя
        ```
        python manage.py createsuperuser
        ```
    7. Собрать статические файлы проекта и приложений в одном месте:
        ```
        python manage.py collectstatic
        ```
    8. На вкладке Web в раздел Static files в поле URL в первой строке записать /static/, во второй /media/. В поле Directory в первой строке /home/username/news_project/city_newsproject/static, во второй /home/username/news_project/city_newsproject/media
    9. В разделе Files в папке news_project/city_newsproject добавить папку log
    10. Перезагрузить сервер

