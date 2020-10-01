import view

siteDirectory = "WWW/"


# {"error_number": ("content_type", "path")}
siteErrorPages = {
    "404 Not Found": ("text/html;charset=utf-8", "errors/404.html")
}

# {"method": {"page_address": ("type", "content_type", "path")}}
sitePages = {
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
