# Lightweight Server

## Описание
Это простой лекговесный асинхронный HTTP сервер, написанный на Python 3.

## Требования
Для запуска потребуется:
+ Python 3.8.6 (было протестировано, может запуститься и на более ранних версиях)
+ Библиотеки:
  + python3-magic (устанавливал через apt)

## Настройка
На данный момент существует один файл настроек: `serverConfig.py`

### Глобальные настройки
+ `SERVER_ON_PORT` - порт, на котором работает сервер. Обычно применяется, когда сервер переходит на TLS/SSL;
+ `USE_SSL` - включает поддержку SSL;
  + Если используется SSL, требуется указать:
    + `SSL_KEYFILE` - путь до файла ключей сертификата;
    + `SSL_CERTFILE` - путь до самого сертификата;

### Настройки расположения файлов сервера-сайта
+ siteDirectory - переменная пути до файлов сервера-сайта. Все указанные пути к файлам в словарях ниже будут ссылаться на файлы в этой папке;
+ siteErrorPages - словарь с путями к HTML страницам HTTP ошибок. Имеет следующий вид:
```python
{
    "<код HTTP ошибки>": ("<MIME тип содержимого>", "<путь до HTML файла>")
}
```
+ sitePages - словарь с путями до файлов.
```python
{
    "<HTTP метод>": {
        "<URL>": ("<тип представления>", *<аргументы>)
    }
}
```
В случае, если используется HTTP метод GET, то аргументы выглядят так:
+ Если тип `file` - `"<MIME тип содержимого>", "<путь до локального файла>"`
+ Если тип `redirection` - `"<адрес в сети или URL>"`
+ Если тип `function` - `"<функция обработки запроса>"`

## Функции для обработки запроса
Свои функции обработки запроса следует размещать в файле `view.py` (можно и в других, тогда следует сделать импортирование модуля в `serverConfig.py`).
Пример:
```python
# view.py
from pageEngine import generateHTTPAnswer


def about():
    # Можно добавить два аргумента в функцию и получить запросы HEAD и BODY
    send_data = "<h1>About</h1>".encode()  # Данные обязательно должны конвертированы в строке байтов

    return generateHTTPAnswer(content_type="text/html", data=send_data)
```

Далее в файл `serverConfig.py`, в словарь `siteMap`, должна быть помещена строка в соответствии с методом (GET, POST и др.), который вы хотите использовать:
```python
# serverConfig.py
import view
...
siteMap = {
    "GET": {
        ...
        "/about": ("function", view.about)
    }
    ...
}
```
После перезапуска сервера, появится новая страница по адресу `/about`.
