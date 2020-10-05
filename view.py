from pageEngine import generateHTTPAnswer, getTemplate


def about(head, body):
    data = getTemplate("about.html")

    if data is not None:
        data = data.decode().format(head=head, body=body)
        return generateHTTPAnswer(content_type="text/html; charset=utf-8", data=data.encode())
    else:
        return generateHTTPAnswer(status="404 Not Found", data=b"")
