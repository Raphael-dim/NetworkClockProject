import socket


def request_time(server_host, server_port, time_format):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_host, server_port))
            request = f"{time_format}\n"
            sock.sendall(request.encode("utf-8"))
            response = sock.recv(1024).decode("utf-8")
            print("Current time:", response)
    except Exception as e:
        print(f"Failed to get time from server: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <time_format>")
        sys.exit(1)

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    time_format = sys.argv[3]

    request_time(server_host, server_port, time_format)
