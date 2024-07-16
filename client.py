import socket


def request_connection(server_host, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_host, server_port))
        while True:
            message = input("Enter the command (or 'exit' to quit): ")
            if message.lower() == "exit":
                break
            # Append a newline character as a delimiter
            sock.sendall((message + "\n").encode("utf-8"))
            response = recv_all(sock)
            print("Response:", response)


def recv_all(sock):
    buffer = ""
    while True:
        data = sock.recv(1024).decode("utf-8")
        buffer += data
        if "\n" in buffer:
            message, buffer = buffer.split("\n", 1)
            return message


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: py client.py <server_host> <server_port>")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])

    request_connection(server_host, server_port)
