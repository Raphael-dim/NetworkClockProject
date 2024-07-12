import os


def get_port():
    config_path = os.path.join(
        os.getenv("USERPROFILE"), "AppData", "Local", "Clock", "port.txt"
    )
    # si le fichier n'est pas trouvé, on créer le dossier et le fichier
    if not os.path.exists(os.path.dirname(config_path)):
        os.makedirs(os.path.dirname(config_path))
        with open(config_path, "w") as file:
            file.write("8080")

    try:
        with open(config_path, "r") as file:
            port = int(file.read().strip())
            return port
    except Exception as e:
        print(f"Error reading port configuration: {e}")
        return 8080  # Default port


if __name__ == "__main__":
    print(f"Configured port: {get_port()}")
