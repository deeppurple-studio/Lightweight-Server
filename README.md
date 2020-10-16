# Lightweight Server

## Описание
Это простой лекговесный асинхронный HTTP сервер, написанный на Python 3.

## Настройка
На данный момент существует один файл настроек: `serverConfig.py`

### Глобальные настройки
* `SERVER_ON_PORT` - порт, на котором работает сервер. Обычно применяется, когда сервер переходит на TLS/SSL;
* `USE_SSL` - включает поддержку SSL;
* `SSL_KEYFILE` - путь до файла ключей сертификата;
* `SSL_CERTFILE` - путь до самого сертификата;

### Настройки расположения файлов сервера-сайта
* siteDirectory - переменная пути до файлов сервера-сайта. Все указанные пути к файлам в словарях ниже будут ссылаться на файлы в этой папке;
* siteErrorPages - словарь с путями к HTML страницам HTTP ошибок. Имеет следующий вид:
```
{
    "<код HTTP ошибки>": ("<тип содержимого>", "<путь до HTML файла>")
}
```
* sitePages - словарь с путями до файлов.
```
{
    "<HTTP метод>": {
        "<URL>": ("<тип>", *<аргументы>)
    }
}
```
В случае, если используется HTTP метод GET, то аргументы могут быть:
* Если тип `file` - `"<тип содержимого файла>", "<путь до локального файла>"`
* Если тип `redirection` - `"<адрес в сети или URL>"`
* Если тип `function` - `"<функция обработки запроса>"`

## Кастомные функции обработки запроса
Свои функции обработки запроса следует размещать в файле `view.py`.
Пример:
```
# view.py
from pageEngine import generateHTTPAnswer


def about():
    # Можно добавить два аргумента в функцию и получить запросы HEAD и BODY
    send_data = "<h1>About</h1>"

    # Данные обязательно должны конвертированы в строке байтов
    return generateHTTPAnswer(content_type="text/html", data=send_data.encode())
```
Далее в файл `serverMap.py`, в словарь `sitePages`, должна быть помещена строка в соответствии с методом (GET, POST и др.), который вы хотите использовать:
```
# serverMap.py
import view
...
sitePages = {
    "GET": {
        ...
        "/about": ("function", view.about)
    }
    ...
}
```
После перезапуска сервера, появится новая страница по адресу `/about`.
