import os

import serverConfig
from libs import Logger


log = Logger.Log("page engine", "print")


def generateHTTPAnswer(status="200 OK", content_type=None, redirection=None, data=None):
    return {"status": status, "content_type": content_type, "redirection": redirection, "data": data}


# Работа с файлами
def getTemplate(filename):
    if os.path.exists(f"{serverConfig.siteDirectory}templates"):
        return readFile(f"templates/{filename}")
    else:
        log.write(f"Template folder not found!", "W")
        return None


def getErrorPage(err_code):
    content_type = None
    data = None

    if err_code in serverConfig.siteErrorPages.keys():
        error_page_file = readFile(serverConfig.siteErrorPages[err_code][1])

        if error_page_file:
            content_type = serverConfig.siteErrorPages[err_code][0]
            data = error_page_file
        else:
            log.write(f"HTTP error file [{err_code}] not found!", "W")

    return {"status": err_code, "content_type": content_type, "data": data}


def readFile(filename):
    if os.path.exists(f"{serverConfig.siteDirectory}{filename}"):
        with open(f"{serverConfig.siteDirectory}{filename}", "rb") as file_:
            data = file_.read()
        return data
    else:
        return None
