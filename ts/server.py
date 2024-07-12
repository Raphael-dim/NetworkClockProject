import datetime
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import subprocess
import os
import socket
import threading
import signal

# Default format in user-friendly form
default_format = "YYYY-MM-dd HH:mm:ss"
# Global variable for current format
current_format = default_format

# Mapping for user-friendly format to strftime-compatible format
format_mapping = {
    "YYYY": "%Y",
    "MM": "%m",
    "dd": "%d",
    "HH": "%H",
    "mm": "%M",
    "ss": "%S",
}

root = tk.Tk()
time_label = tk.Label(root, text="", font=("Courier", 24), fg="white", bg="black")


def convert_to_strftime_format(user_format):
    for key, value in format_mapping.items():
        user_format = user_format.replace(key, value)
    return user_format


def update_label_time():
    current_time = datetime.datetime.now().strftime(
        convert_to_strftime_format(current_format)
    )
    time_label.config(text=current_time)


def create_gui():
    def edit_date_time():
        selected_date = cal.get_date()
        selected_time = datetime.time(
            int(hour_var.get()), int(minute_var.get()), int(second_var.get())
        )
        new_time = datetime.datetime.combine(selected_date, selected_time)

        print(new_time)
        ts_script_path = os.path.join(os.path.dirname(__file__), "set_system_time.py")
        print(ts_script_path)
        if not os.path.isfile(ts_script_path):
            raise FileNotFoundError(f"{ts_script_path} not found")

        date_str = new_time.strftime("%Y-%m-%d")
        time_str = new_time.strftime("%H:%M:%S")

        if os.name == "nt":
            powershell_cmd = [
                "powershell.exe",
                "-Command",
                f"Start-Process py -ArgumentList '{ts_script_path}', '{date_str}', '{time_str}' -Verb RunAs",
            ]
            subprocess.check_call(" ".join(powershell_cmd), shell=True)
        else:
            subprocess.check_call(
                ["sudo", "python3", ts_script_path, date_str, time_str]
            )

        update_label_time()

    def update_format():
        global current_format
        new_format = format_entry.get()
        try:
            datetime.datetime.now().strftime(convert_to_strftime_format(new_format))
            current_format = new_format
            update_label_time()
        except ValueError:
            messagebox.showerror("Error", "Invalid format specified")

    def reset_format():
        global current_format
        current_format = default_format
        format_entry.delete(0, tk.END)
        format_entry.insert(0, default_format)
        update_label_time()

    root.title("Set System Time")
    root.configure(background="black")
    root.geometry("500x500")

    time_label.pack(pady=20)

    edit_format_frame = tk.Frame(
        root,
        bg="black",
        bd=0,
        relief=tk.SOLID,
        highlightbackground="white",
        highlightthickness=2,
    )

    edit_format_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    edit_format_label = tk.Label(
        edit_format_frame,
        text="Edit Format",
        font=("Arial", 14),
        fg="white",
        bg="black",
    )
    edit_format_label.pack(pady=10)
    format_entry = tk.Entry(edit_format_frame, width=50)
    format_entry.pack(pady=10)
    format_entry.insert(0, default_format)

    update_button = tk.Button(
        edit_format_frame, text="Update Format", command=update_format
    )
    update_button.pack(pady=10)
    reset_button = tk.Button(edit_format_frame, text="Reset", command=reset_format)
    reset_button.pack(pady=10, padx=10)

    edit_frame = tk.Frame(
        root,
        bg="black",
        bd=0,
        relief=tk.SOLID,
        highlightbackground="white",
        highlightthickness=2,
    )

    edit_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    edit_label = tk.Label(
        edit_frame, text="Edit Date/Time", font=("Arial", 14), fg="white", bg="black"
    )
    edit_label.pack(pady=10)

    cal = DateEntry(
        edit_frame, width=12, background="white", foreground="black", borderwidth=2
    )
    cal.pack(padx=10, pady=10)

    time_frame = tk.Frame(edit_frame, bg="black")
    time_frame.pack(padx=10, pady=10)

    hour_var = tk.StringVar(value=datetime.datetime.now().hour)
    minute_var = tk.StringVar(value=datetime.datetime.now().minute)
    second_var = tk.StringVar(value=datetime.datetime.now().second)

    hour_label = tk.Label(time_frame, text="Hour:", fg="white", bg="black")
    hour_label.grid(row=0, column=0, padx=5, pady=5)
    hour_entry = tk.Spinbox(time_frame, from_=0, to=23, textvariable=hour_var, width=5)
    hour_entry.grid(row=0, column=1, padx=5, pady=5)

    minute_label = tk.Label(time_frame, text="Minute:", fg="white", bg="black")
    minute_label.grid(row=0, column=2, padx=5, pady=5)
    minute_entry = tk.Spinbox(
        time_frame, from_=0, to=59, textvariable=minute_var, width=5
    )
    minute_entry.grid(row=0, column=3, padx=5, pady=5)

    second_label = tk.Label(time_frame, text="Second:", fg="white", bg="black")
    second_label.grid(row=0, column=4, padx=5, pady=5)
    second_entry = tk.Spinbox(
        time_frame, from_=0, to=59, textvariable=second_var, width=5
    )
    second_entry.grid(row=0, column=5, padx=5, pady=5)

    validate_button = tk.Button(edit_frame, text="Validate", command=edit_date_time)
    validate_button.pack(pady=10)

    update_label_time()

    def update_time():
        update_label_time()
        root.after(1000, update_time)

    update_time()

    root.mainloop()


def handle_client(client_socket):
    try:
        while True:
            request = client_socket.recv(1024).decode("utf-8")
            if not request:
                break
            if request.strip().lower() == "exit":
                break
            formatted_time = get_formatted_time(request.strip())
            client_socket.send(formatted_time.encode("utf-8"))
    except Exception as e:
        print(f"Error handling client: {e}")


def get_formatted_time(format_string="YYYY-mm-dd HH:MM:SS"):
    now = datetime.datetime.now()
    try:
        return now.strftime(convert_to_strftime_format(format_string))
    except Exception as e:
        return f"Error formatting time: {e}"


def start_server(stop_event):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = get_port()
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"[*] Listening on port {port}")

    server.settimeout(1.0)  # Set a timeout for accepting connections
    while not stop_event.is_set():
        try:
            client_socket, addr = server.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
            client_handler = threading.Thread(
                target=handle_client, args=(client_socket,)
            )
            client_handler.start()
        except socket.timeout:
            continue
    server.close()


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


def signal_handler(sig, frame):
    print("Exiting...")
    stop_event.set()
    root.quit()  # Stop the GUI loop


if __name__ == "__main__":
    stop_event = threading.Event()

    signal.signal(signal.SIGINT, signal_handler)

    server_thread = threading.Thread(target=start_server, args=(stop_event,))
    server_thread.start()

    create_gui()

    server_thread.join()
