import socket
import threading
from .settings import get_port
from .clock import get_formatted_time
from .privileges import drop_privileges


def handle_client(client_socket):
    try:
        while True:
            request = client_socket.recv(1024).decode("utf-8")
            if not request:
                break
            formatted_time = get_formatted_time(request.strip())
            client_socket.send(formatted_time.encode("utf-8"))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


def start_server():
    drop_privileges()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = get_port()
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"[*] Listening on port {port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()
