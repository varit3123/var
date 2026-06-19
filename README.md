# Водить.РФ Django

Проект разложен по экзаменационным блокам:

- `module-1` - отдельный Django-проект первой части;
- `module-2` - отдельный Django-проект второй части.

## Как запускать на другом localhost/порту

Формат команды:

```bash
py manage.py runserver IP:PORT
```

Примеры:

```bash
py manage.py runserver 127.0.0.1:8000
py manage.py runserver 127.0.0.1:8001
py manage.py runserver localhost:8080
```

Если нужно открыть сайт с другого устройства в одной сети:

```bash
py manage.py runserver 0.0.0.0:8000
```

## Запуск модуля 1

```bash
cd module-1
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py seed_demo
py manage.py runserver 127.0.0.1:8001
```

Открыть: `http://127.0.0.1:8001/module-1/`

## Запуск модуля 2

```bash
cd module-2
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py seed_demo
py manage.py runserver 127.0.0.1:8000
```

Открыть: `http://127.0.0.1:8000/module-2/`

## Доступы

- Администратор: `Admin26` / `Demo20`
- Пользователь: `demo26` / `Demo2026`
- Дополнительный пользователь: `anna26` / `River2026`

Данные хранятся в SQLite через Django ORM. Демо-данные создаются командой `py manage.py seed_demo`.
