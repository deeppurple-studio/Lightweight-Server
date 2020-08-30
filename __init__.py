import socket
import select

import handler
from libs import Logger


def accept_connection(sock):
    conn, addr = sock.accept()
    to_monitor.append(conn)

    log.write(f"New connection from {addr[0]}")


def handle_connection(sock):
    handler.Handle(sock)


def event_loop():
    while True:
        for sock in to_monitor:
            if sock.fileno == -1:
                to_monitor.remove(sock)
                log.write("Remove socket with bad file descryptor", "W")

        ready_to_read = select.select(to_monitor, [], [])[0]

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                handle_connection(sock)


if __name__ == "__main__":
    log = Logger.Log("init", "print")
    
    try:
        to_monitor = []

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        server_socket.bind(("0.0.0.0", 80))
        server_socket.listen()

        to_monitor.append(server_socket)
        event_loop()
    except Exception as ex:
        import traceback

        log.write(f"{ex}!!!", "E")
        traceback.print_tb(ex.__traceback__)
    except KeyboardInterrupt:
        log.write(f"Emergency stop (keyboard interrupt)", "W")
    finally:
        log.close()
