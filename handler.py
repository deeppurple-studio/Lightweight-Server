test_webpage = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8"/>
        <title>Server is work</title>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
        <h1>Please wait when server is run</h1>
        <hr />
        <div>Status: 200 OK</div>
    </body>
</html>"""


def send_answer(conn, status="200 OK", content_type="text/plain; charset=utf-8", data=b""):
    data_length = len(data)

    answer = f"HTTP/1.1 {status}\r\n"
    answer += "Server: LightServer\r\n"
    answer += f"Content-Type: {content_type}\r\n"
    answer += f"Content-Length: {data_length}\r\n"
    answer += "\r\n\r\n"

    http_packet = answer.encode("utf-8") + data

    conn.send(http_packet)


def Handler(conn):
    raw_data = conn.recv(1024)
    
    if not raw_data:
        return

    decode_data = raw_data.decode("utf-8")
    head_request, body_request = decode_data.split("\r\n\r\n", 2)

    request_title = head_request.split("\r\n")[0]
    print(request_title, end=";")

    method, address, protocol = request_title.split(" ", 3)
    print(protocol)

    if protocol == "HTTP/1.0" or protocol == "HTTP/1.1":
        if method == "GET":
            if address == "/" or address == "/index":
                send_answer(conn, content_type="text/html; charset=utf-8", data=test_webpage.encode("utf-8"))
            else:
                send_answer(conn, status="404 Not Found")
        elif method == "POST":
            pass
        else:
            send_answer(conn, status="501 Not Implemented")
    else:
        send_answer(conn, status="505 HTTP Version Not Supported")

