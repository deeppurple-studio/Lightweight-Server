from pageEngine import generateCustomAnswer, getTemplateFromFile
import serverConfig


def about(head, body):
    data = getTemplateFromFile("about.html")

    if data is not None:
        data = data.decode().format(head=head, body=body)
        return generateCustomAnswer(content_type="text/html; charset=utf-8", data=data.encode())
    else:
        return generateCustomAnswer(status="404 Not Found", data=b"")


urls_GET = {
    "/index.html": ("file", "text/html;charset=utf-8", "index.html"),
    "/": ("redirection", "/index.html"),

    "/about": ("function", about)
}

# Добавляем функцию в структуру сайта
serverConfig.SITE_STRUCTURE["GET"].update(urls_GET)

# Для добавления целой папки в карту сайта (автоматическое обновление не работает, требуется перезапуск сервера):
# SITE_STRUCTURE["GET"].update(pageEngine.generateFilesTreeFromFolder("<путь_до_папки_внутри_siteDirectory>"))
