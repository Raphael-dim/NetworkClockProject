import socket


def request_connection(server_host, server_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_host, server_port))
            while True:
                message = input("Enter the command (or 'exit' to quit): ")
                if message.lower() == "exit":
                    break
                sock.sendall(message.encode("utf-8"))
                response = sock.recv(1024).decode("utf-8")
                print("Response:", response)
    except Exception as e:
        print(f"Failed to communicate with server: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python client.py <server_host> <server_port>")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])

    request_connection(server_host, server_port)
