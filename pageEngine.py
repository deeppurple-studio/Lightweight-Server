def checkIndexSitePages():
    # TODO: create checking site index
    pass


def checkErrorPageFile(error_code):
    # TODO: move check error pages file from handlers.methodHandler
    pass


def readFile(filename):
    with open(filename, "r") as file_descryptor:
        data = file_descryptor.read()

    return data
