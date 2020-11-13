import socket
import ssl
import select

import serverConfig
import handlers
from libs import Logger


def acceptConnection(sock):
    # Принимаем входящие подключения
    try:
        conn, addr = sock.accept()
    except ssl.SSLError as ex:
        err_str = ""

        for item in ex.args:
            if type(item) is str:
                err_str += item

        if "[SSL: TLSV1_ALERT_UNKNOWN_CA]" in err_str:
            # Если у вас самоподписанный сертификат
            log.write("TLSv1 alert: unknown CA!\n | You certificate self-signed?\n | Please do use trusted Certificate center", "W")
        elif "[SSL: WRONG_VERSION_NUMBER]" in err_str:
            # Перехватываем ошибку, если клиент использует другой протокол (SSL вместо TLS)
            pass
        else:
            # HACK: переват ошибок связанных с SSL
            log.write(f"{err_str}", "W")
    except Exception as ex:
        # TOFIX: по хорошему, мы не должны перехватывать все ошибки,
        # связанные с сокетами. Сделано для отладки и что бы сервер не крашился
        log.write(f"Err: {ex}")
    else:
        to_monitor.append(conn)
        log.write(f"New connection from {addr[0]}")


def eventLoop():
    while True:
        for sock in to_monitor:
            # Очищаем список от сокетов с закрытым дескриптором
            if sock.fileno == -1:
                to_monitor.remove(sock)
                log.write("Remove socket with bad file descryptor")

        ready_to_read = select.select(to_monitor, [], [])[0]

        for sock in ready_to_read:
            if sock is server_socket:
                acceptConnection(sock)
            else:
                handlers.parseHandler(sock)


if __name__ == "__main__":
    log = Logger.Log("init", "print")

    try:
        to_monitor = []

        if serverConfig.USE_SSL:
            server_socket = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), serverConfig.SSL_KEYFILE, serverConfig.SSL_CERTFILE, True)
        else:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Даем возможность переиспользовать адрес
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        server_socket.bind(("0.0.0.0", serverConfig.SERVER_ON_PORT))
        server_socket.listen()

        to_monitor.append(server_socket)
        eventLoop()
    except Exception as ex:
        import traceback

        log.write(f"{ex}!!!", "E")
        traceback.print_tb(ex.__traceback__)
    except KeyboardInterrupt:
        log.write(f"Emergency stop (keyboard interrupt)", "W")
    finally:
        log.close()
