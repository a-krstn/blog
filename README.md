# Blog

## Содержание
- [О проекте](#о-проекте)
- [Стек](#стек)
- [Начало работы](#начало-работы)

## О проекте
Простое приложение для ведения личного блога с системой комментариев.

## Стек
- Django
- PostgreSQL

## Начало работы
1. **Клонирование приложения**<br>
   `git clone git@github.com:a-krstn/blog.git`
2. **Создание виртуального окружения и его активация**<br>
   В командной строке из директории проекта<br>
   `python -m venv .venv`<br>
   - Windows: `.venv\Scripts\activate`<br>
   - Linux/MacOS: `source .venv/bin/activate`
3. **Установка зависимостей**<br>
   `pip install -r mysite/requirements.txt`
4. **Запуск приложения**<br>
   Для запуска сервера выполнить команду:<br>
   `python manage.py runserver`<br>
   Приложение будет доступно по адресу http://127.0.0.1:8000/