import os


def get_port():
    # on récupére le port dans le fichier config/port.txt
    # on utilise le délimiteur tcp_port = pour récupérer la valeur
    port = 8080
    portTxtFile = os.path.join(os.path.dirname(__file__), "config", "port.txt")
    if os.path.exists(portTxtFile):
        with open(portTxtFile, "r") as file:
            for line in file:
                if "tcp_port =" in line:
                    port = int(line.split("=")[1].strip())
                    break

    config_path = os.path.join(
        os.getenv("USERPROFILE"), "AppData", "Local", "Clock", "port.txt"
    )
    # si le fichier n'est pas trouvé, on créer le dossier et le fichier
    if not os.path.exists(os.path.dirname(config_path)):
        os.makedirs(os.path.dirname(config_path))
        with open(config_path, "w") as file:
            file.write(str(port))

    try:
        with open(config_path, "r") as file:
            port = int(file.read().strip())
            return port
    except Exception as e:
        print(f"Error reading port configuration: {e}")
        return 8080  # Default port


if __name__ == "__main__":
    print(f"Configured port: {get_port()}")
