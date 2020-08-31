import os

import siteMap

from libs import Logger


log = Logger.Log("page engine", "print")


def checkSiteIndex():
    # TODO: create checking site index
    pass


def getErrorPage(err_code):
    content_type = None
    data = None

    if err_code in siteMap.siteErrorPages.keys():
        error_page_file = readFile(siteMap.siteErrorPages[err_code][1])
 
        if error_page_file:
            content_type = siteMap.siteErrorPages[err_code][0]
            data = error_page_file
        else:
            log.write(f"Error file [{err_code}] not found!", "W")

    return { "status":err_code, "content_type":content_type, "data":data }


def readFile(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as file_descryptor:
            data = file_descryptor.read()
        return data
    else:
        return None
