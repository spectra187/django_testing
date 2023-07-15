# Django testing

## Описание
Коллекция тестов для проектов YaNews и YaNote на pytest и unittest.


### Тесты на pytest для проекта YaNews


## Установка и запуск

**ВЕРСИЯ Python3.9**

Клонировать репозиторий:
```sh
git clone <https or SSH URL>
```

Перейти в корневую папку:
```sh
cd django_testing
```

Создать и активировать виртуальное окружение:
```sh
python -m venv venv
source venv/Scripts/activate
```

Обновить pip:
```sh
python -m pip install --upgrade pip
```

Установить библиотеки:
```sh
pip install -r requirements.txt
```

Выполнить миграции для каждого проекта:
```sh
python ya_news/manage.py migrate
python ya_note/manage.py migrate
```

Загрузить фикстуры DB для ya_news:
```sh
python ya_news/manage.py loaddata ya_news/news/fixtures/news.json
```

Перейти в папку необходимого проекта. Запустить тесты для проектов:
```sh
# YaNews
cd ../ya_news
pytest

# YaNote
cd ../ya_note
pytest
```

