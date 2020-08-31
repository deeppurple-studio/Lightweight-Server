import siteMap
import pageEngine

from libs import Logger


SUPPORT_METHODS = ("GET", "POST", "PUT", "DELETE")
SUPPORT_PROTOCOLS = ("HTTP/1.0", "HTTP/1.1")


log = Logger.Log("handler", "print,file")


def sendAnswer(conn, status="200 OK", content_type=None, redirection=None, data=None):
    if not content_type:
        content_type = "text/plain; charset=utf-8"

    if not data:
        data = b""

    data_length = len(data)

    answer = f"HTTP/1.1 {status}\r\n"
    answer += "Server: LightServer\r\n"
    if redirection:
        answer += f"Location: {redirection}\r\n"
    answer += f"Content-Type: {content_type}\r\n"
    answer += f"Content-Length: {data_length}\r\n"
    answer += "\r\n\r\n"

    http_packet = answer.encode("utf-8") + data

    conn.send(http_packet)


def connectionsHandler(conn):
    raw_data = conn.recv(1024)

    if not b"\r\n\r\n" in raw_data:
        return

    head_request, body_request = raw_data.split(b"\r\n\r\n", 2)
    head_request = head_request.decode("utf-8")

    request_title = head_request.split("\r\n")[0]
    log.write(request_title)

    method, address, protocol = request_title.split(" ", 3)

    if protocol in SUPPORT_PROTOCOLS:
        methodHandler(conn, method, address, body_request)
    else:
        page = pageEngine.getErrorPage("505 HTTP Version Not Supported")
        sendAnswer(conn, status=page["status"], content_type=page["content_type"], data=page["data"])


def methodHandler(conn, method, address, body_request):
    if method in SUPPORT_METHODS and method in siteMap.sitePages.keys():
            if address == "/" or address == "/index":
                # TODO page generator :)
                sendAnswer(conn, content_type="text/html; charset=utf-8", data="<h1>Hi</h1>".encode("utf-8"))
 
            else:
                page = pageEngine.getErrorPage("404 Not Found")
                sendAnswer(conn, status=page["status"], content_type=page["content_type"], data=page["data"])

    else:
        page = pageEngine.getErrorPage("501 Not Implemented")
        sendAnswer(conn, status=page["status"], content_type=page["content_type"], data=page["data"])
