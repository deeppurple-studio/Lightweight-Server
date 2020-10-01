from pageEngine import generateHTTPAnswer

def about(head, body):
    data = "<!DOCTYPE html><html><body><h1>About</h1><div>{}</div><div>{}</div></body></html>"
    data = data.format(head, body)
    
    return generateHTTPAnswer(content_type="text/html; charset=utf-8", data=data.encode())
