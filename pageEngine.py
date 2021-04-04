import os

import serverConfig
from libs import Logger

if serverConfig.USE_MAGIC_LIB:
    import magic

log = Logger.Log("page engine", output_type="console")


def generateCustomAnswer(status="200 OK", content_type=None, redirection=None, data=None):
    """ Требуется для правильной генерации ответа сервера """
    answer = {
        "status": status,
        "content_type": content_type,
        "redirection": redirection,
        "data": data
    }

    return answer


# Работа с файлами
def getTemplateFromFile(filename):
    if os.path.exists(f"{serverConfig.SITE_DIR}templates"):
        return readFile(f"templates/{filename}")
    else:
        log.write(f"Директория шаблонов [{serverConfig.SITE_DIR}templates] отсутствует.", "W")
        return None


def generateFilesTreeFromFolder(folder):
    """
    Вывод всех путей до файлов в папке
    """
    if serverConfig.USE_MAGIC_LIB:
        if os.path.exists(f"{serverConfig.SITE_DIR}{folder}"):
            filesInTree = {}
            mime = magic.Magic(mime=True)

            for path, folders, filesList in os.walk(f"{serverConfig.SITE_DIR}{folder}"):
                for fileName in filesList:
                    fullFilePath = f"{path}/{fileName}".replace("//", "/")
                    relFilePath = fullFilePath.replace(f"{serverConfig.SITE_DIR}", "")

                    if fileName.split(".")[-1] == "css":                                                                                                   
                        mimeType = "text/css"
                    else:
                        mimeType = mime.from_file(fullFilePath)

                    filesInTree.update({f"/{relFilePath}": ("file", mimeType, f"{relFilePath}")})
            return filesInTree
        else:
            log.write(f"Создание дерева каталога [{folder}] невозможно. Директория отсутствует", "W")
            return None
    else:
        log.write("Библиотека magic не используется. Вывод всех путей до файлов в папке невозможен.", "E")
        return None


def generateErrorAnswerFromFile(err_code):
    content_type = None
    data = None

    if err_code in serverConfig.SITE_ERROR_FILES.keys():
        error_page_file = readFile(serverConfig.SITE_ERROR_FILES[err_code][1])

        if error_page_file:
            content_type = serverConfig.SITE_ERROR_FILES[err_code][0]
            data = error_page_file
        else:
            log.write(f"HTTP error file [{err_code}] not found!", "W")

    return {"status": err_code, "content_type": content_type, "data": data}


def readFile(filename):
    if os.path.exists(f"{serverConfig.SITE_DIR}{filename}"):
        with open(f"{serverConfig.SITE_DIR}{filename}", "rb") as file_:
            data = file_.read()
        return data
    else:
        return None
