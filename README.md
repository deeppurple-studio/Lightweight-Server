# Lightweight Server

## Описание
Это простой лекговесный асинхронный HTTP сервер, написанный на Python 3.

## Настройка
На данный момент существует один файл настроек: `siteMap.py`

Структура:
* siteDirectory - переменная пути до файлов сервера. Все указанные пути к файлам в словарях ниже будут ссылаться на файлы в этой папке.
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
* [На этапе разработки] Если тип `function` - `"<функция обработки запроса>"`