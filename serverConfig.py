# --- Глобальные настройки ---
SERVER_ON_PORT = 443

USE_SSL = True

SSL_KEYFILE = "certificate/server.key"
SSL_CERTFILE = "certificate/server.crt"


# --- Настройки сайта ---
import view


siteDirectory = "WWW/"

# {"error_number": ("content_type", "path")}
siteErrorPages = {
    "404 Not Found": ("text/html;charset=utf-8", "errors/404.html")
}

# {"method": {"page_address": ("type", "content_type", "path")}}
siteMap = {
    "GET": {
        # If type:
        #   "file" - read data from file and send to client
        #   "redirection" - send redirect address to client
        #   "function" - execute function and send data (from return) to client

        "/index.html": ("file", "text/html;charset=utf-8", "index.html"),
        "/": ("redirection", "/index.html"),
        "/about": ("function", view.about)
    }
}
