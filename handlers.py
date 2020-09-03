import siteMap
import pageEngine

from libs import Logger


SUPPORT_PROTOCOLS = ("HTTP/1.0", "HTTP/1.1")


log = Logger.Log("handler", "print,file")


def sendAnswer(conn, status="200 OK", content_type=None, redirection=None, data=None):
    if content_type is None:
        content_type = "text/plain; charset=utf-8"

    if data is None:
        data = b""

    data_length = len(data)

    answer = f"HTTP/1.1 {status}\r\n"
    answer += "Server: LightServer\r\n"
    if redirection is not None:
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

    head, body_request = raw_data.split(b"\r\n\r\n", 2)
    head = head.decode("utf-8")

    request_title = head.split("\r\n")[0]

    method, address, protocol = request_title.split(" ", 3)

    if protocol in SUPPORT_PROTOCOLS:
        head_request = None

        if "?" in address:
            address, head_request = address.split("?", 2)

        methodHandler(conn, method, address, head_request, body_request)
    else:
        page = pageEngine.getErrorPage("505 HTTP Version Not Supported")
        sendAnswer(conn, status=page["status"], content_type=page["content_type"], data=page["data"])


def methodHandler(conn, method, address, head_request, body_request):
    log.write(f"Method: {method}, Addr: {address}")
    if method in siteMap.sitePages.keys():
            if address in siteMap.sitePages[method].keys():
                page_info = siteMap.sitePages[method][address]

                if len(page_info) > 1:
                    if page_info[0] == "file" and len(page_info) == 3:
                        file_ = pageEngine.readFile(page_info[2])

                        if file_ is None:
                            page = pageEngine.getErrorPage("404 Not Found")
                            sendAnswer(conn, status=page["status"], content_type=page["content_type"], data=page["data"])
                        else:
                            sendAnswer(conn, content_type=page_info[1], data=pageEngine.readFile(page_info[2]))
                    elif page_info[0] == "redirection" and len(page_info) == 2:
                        sendAnswer(conn, status="308 Permanent Redirect", redirection=page_info[1])
                    elif page_info[0] == "function" and len(page_info) == 2:
                        #page_data = page_info[1]()
                        #sendAnswer()
                        pass

            else:
                page = pageEngine.getErrorPage("404 Not Found")
                sendAnswer(conn, status=page["status"], content_type=page["content_type"], data=page["data"])

    else:
        page = pageEngine.getErrorPage("501 Not Implemented")
        sendAnswer(conn, status=page["status"], content_type=page["content_type"], data=page["data"])
