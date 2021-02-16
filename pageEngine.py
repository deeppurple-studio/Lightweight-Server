import os

import magic

import serverConfig
from libs import Logger


log = Logger.Log("page engine", "print")


def generateHTTPAnswer(status="200 OK", content_type=None, redirection=None, data=None):
    answer = {
        "status": status,
        "content_type": content_type,
        "redirection": redirection,
        "data": data
    }

    return answer


# Работа с файлами
def getTemplate(filename):
    if os.path.exists(f"{serverConfig.siteDirectory}templates"):
        return readFile(f"templates/{filename}")
    else:
        log.write(f"Template folder not found!", "W")
        return None


def generateFilesTreeFromFolder(folder):
    """
    Вывод всех путей до файлов в папке
    """
    if os.path.exists(f"{serverConfig.siteDirectory}{folder}"):
        filesInTree = {}
        mime = magic.Magic(mime=True)

        for path, folders, filesList in os.walk(f"{serverConfig.siteDirectory}{folder}"):
            for fileName in filesList:
                fullFilePath = f"{path}/{fileName}".replace("//", "/")
                relFilePath = fullFilePath.replace(f"{serverConfig.siteDirectory}", "")

                if fileName.split(".")[-1] == "css":                                                                                                   
                    mimeType = "text/css"
                else:
                    mimeType = mime.from_file(fullFilePath)

                filesInTree.update({f"/{relFilePath}": ("file", mimeType, f"{relFilePath}")})
        return filesInTree
    else:
        log.write("Can't create folder tree!", "W")
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
