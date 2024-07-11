import os


def get_port():
    config_path = os.path.join(
        os.getenv("USERPROFILE"), "AppData", "Local", "Clock", "port.txt"
    )
    try:
        with open(config_path, "r") as file:
            port = int(file.read().strip())
            return port
    except Exception as e:
        print(f"Error reading port configuration: {e}")
        return 8080  # Default port


if __name__ == "__main__":
    print(f"Configured port: {get_port()}")
