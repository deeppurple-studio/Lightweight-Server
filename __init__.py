import socket
import select


def accept_connections(sock):
    conn, addr = sock.accept()
    to_monitor.append(conn)


def handle_connection(sock):
    print(sock.recv(1024))


def event_loop():
    while True:
        ready_to_read = select.select(to_monitor, [], [])[0]

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                handle_connection(sock)


if __name__ == "__main__":
    to_monitor = []

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind(("0.0.0.0", 80))
    server_socket.listen()

    to_monitor.append(server_socket)
    event_loop()
