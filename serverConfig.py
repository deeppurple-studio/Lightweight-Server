import view


# --- Глобальные настройки ---
SERVER_ON_PORT = 443  # Порт, на котором висит сервер

USE_SSL = True  # Флаг включения поддержки шифрования (TLS)

SSL_KEYFILE = "certificate/server.key"  # Путь до key-файла
SSL_CERTFILE = "certificate/server.crt"  # Путь до файла-сертификата


# --- Настройки сайта ---
siteDirectory = "WWW/"

# Список ошибок и путь до HTML файла
# {"<HTTP ошибка>": ("<MIME тип содержимого>", "<путь до файла>")}
siteErrorPages = {
    "404 Not Found": ("text/html;charset=utf-8", "errors/404.html")
}

# Карта сайта
# {"<метод>": {"<URL>": ("<тип представления>", <аргументы>)}}
siteMap = {
    "GET": {
        # Если тип:
        #   "file" - считываем данные из файла и отправляем клиенту
        #   "redirection" - отправляем адрес перенаправления клиенту
        #   "function" - выполняем функцию и отправляем ее результат

        "/index.html": ("file", "text/html;charset=utf-8", "index.html"),
        "/": ("redirection", "/index.html"),
        "/about": ("function", view.about)
    }
}
