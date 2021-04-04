# --- Глобальные настройки ---
SERVER_ON_PORT = 8080  # Порт, на котором висит сервер

USE_SSL = False  # Флаг включения поддержки шифрования (TLS)

SSL_KEYFILE = "certificate/server.key"  # Путь до key-файла
SSL_CERTFILE = "certificate/server.crt"  # Путь до файла-сертификата


# --- Настройки сайта ---
SITE_DIR = "WWW/"

# Список ошибок и путь до HTML файла
# {"<HTTP ошибка>": ("<MIME тип содержимого>", "<путь до файла>")}
SITE_ERROR_FILES = {
    "404 Not Found": ("text/html;charset=utf-8", "errors/404.html")
}

# Структура сайта
# {"<метод>": {"<URL>": ("<тип представления>", <аргументы>)}}
SITE_STRUCTURE = {
    "GET": {
        # Если тип:
        #   "file" - считываем данные из файла и отправляем клиенту
        #   "redirection" - отправляем адрес перенаправления клиенту
        #   "function" - выполняем функцию и отправляем ее результат

        "/index.html": ("file", "text/html;charset=utf-8", "index.html"),
        "/": ("redirection", "/index.html"),
    }
}

# Используем ли библиотеку для автоматического определения MIME-типа файла
USE_MAGIC_LIB = False
