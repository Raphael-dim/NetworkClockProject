import ctypes
import datetime
import sys
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
    """Converts a user-friendly date/time format to strftime-compatible format.

    Args:
        user_format (str): User-provided date/time format using custom tokens (e.g., YYYY, MM, dd).

    Returns:
        str: A date/time format string converted to strftime-compatible format.

    This function translates a user-specified format into a format compatible with strftime,
    which is a standard way to format date/time in Python. It uses a predefined mapping
    (format_mapping) to replace custom tokens with their respective strftime equivalents.

    For example, if the user provides 'YYYY-MM-dd HH:mm:ss', this function converts it to '%Y-%m-%d %H:%M:%S',
    which strftime understands and can use to format the current date and time accordingly.

    Note: Using strftime is generally safe for formatting purposes. However, if the user is allowed
    to input arbitrary format strings and those strings are used elsewhere (e.g., in a database query),
    additional validation and sanitization might be needed to prevent SQL injection or other security risks.
    """

    for key, value in format_mapping.items():
        user_format = user_format.replace(key, value)
    return user_format


def update_label_time():
    """Update the time displayed on the label."""
    current_time = datetime.datetime.now().strftime(
        convert_to_strftime_format(current_format)
    )
    time_label.config(text=current_time)


def drop_privileges():
    """Drop unnecessary privileges on Windows."""
    try:
        # Adjusting token privileges to drop unnecessary privileges
        # Only necessary if your script started with elevated privileges
        if ctypes.windll.shell32.IsUserAnAdmin() != 0:
            # Check if running with elevated privileges
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit(0)
    except Exception as e:
        print(f"Error dropping privileges: {e}")


def subscribe_to_dep():
    """Subscribe to Data Execution Prevention (DEP)."""
    try:
        if os.name == "nt":
            ctypes.windll.kernel32.SetProcessDEPPolicy(1)
    except Exception as e:
        print(f"Error subscribing to DEP: {e}")


def create_gui():
    def edit_date_time():
        """Set the system time based on user input."""
        selected_date = cal.get_date()

        # Validate the hour (0-23), minute (0-59), and second (0-59)
        if not hour_var.get().isdigit() or not 0 <= int(hour_var.get()) <= 23:
            messagebox.showerror("Error", "Invalid hour specified")
            return
        if not minute_var.get().isdigit() or not 0 <= int(minute_var.get()) <= 59:
            messagebox.showerror("Error", "Invalid minute specified")
            return
        if not second_var.get().isdigit() or not 0 <= int(second_var.get()) <= 59:
            messagebox.showerror("Error", "Invalid second specified")
            return

        selected_time = datetime.time(
            int(hour_var.get()), int(minute_var.get()), int(second_var.get())
        )
        new_time = datetime.datetime.combine(selected_date, selected_time)

        ts_script_path = os.path.join(os.path.dirname(__file__), "set_system_time.py")
        if not os.path.isfile(ts_script_path):
            raise FileNotFoundError(f"{ts_script_path} not found")

        date_str = new_time.strftime("%Y-%m-%d")
        time_str = new_time.strftime("%H:%M:%S")

        if os.name == "nt":
            threading.Thread(
                target=ctypes.windll.shell32.ShellExecuteW,
                args=(
                    None,
                    "runas",
                    sys.executable,
                    f"{ts_script_path} {date_str} {time_str}",
                    None,
                    1,
                ),
            ).start()
        else:
            subprocess.check_call(
                ["sudo", "python3", ts_script_path, date_str, time_str]
            )

        update_label_time()

    def update_format():
        """Update the format used to display the time."""
        global current_format
        new_format = format_entry.get()
        try:
            datetime.datetime.now().strftime(convert_to_strftime_format(new_format))
            current_format = new_format
            update_label_time()
        except ValueError:
            messagebox.showerror("Error", "Invalid format specified")

    def reset_format():
        """Reset the format to the default."""
        global current_format
        current_format = default_format
        format_entry.delete(0, tk.END)
        format_entry.insert(0, default_format)
        update_label_time()

    root.title("Set System Time")
    root.configure(background="black")
    root.geometry("500x550")

    time_label.pack(pady=20)

    time_update_button = tk.Button(root, text="Update Time", command=update_label_time)
    time_update_button.pack(pady=10)

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
    """Handle incoming client connections."""
    buffer = ""
    while True:
        data = client_socket.recv(1024).decode("utf-8")
        if not data:
            break
        buffer += data
        while "\n" in buffer:
            request, buffer = buffer.split("\n", 1)
            if request.strip().lower() == "exit":
                client_socket.close()
                return
            formatted_time = get_formatted_time(request.strip())
            client_socket.sendall((formatted_time + "\n").encode("utf-8"))


def get_formatted_time(format_string="YYYY-mm-dd HH:MM:SS"):
    """Get the current time formatted according to the specified format string."""
    return datetime.datetime.now().strftime(convert_to_strftime_format(format_string))


def start_tcp_server():
    """Start the TCP server to handle client requests."""
    print("Starting TCP server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = get_port()
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


def get_port():
    # on récupére le port dans le fichier config/port.txt
    # on utilise le délimiteur tcp_port = pour récupérer la valeur
    portConfig = 8080
    portTxtFile = os.path.join(os.path.dirname(__file__), "../config", "port.txt")
    if os.path.exists(portTxtFile):
        with open(portTxtFile, "r") as file:
            for line in file:
                if "tcp_port =" in line:
                    portConfig = int(line.split("=")[1].strip())
                    break

    config_path = os.path.join(
        os.getenv("USERPROFILE"), "AppData", "Local", "Clock", "port.txt"
    )

    # si le fichier n'est pas trouvé, on créer le dossier et le fichier
    if not os.path.exists(os.path.dirname(config_path)):
        os.makedirs(os.path.dirname(config_path))
        with open(config_path, "w") as file:
            file.write(str(portConfig))

    # si le fichier est trouvé, on li le port et on compare avec le port de config, si différent on met à jour
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            port = int(file.read())
            if port != portConfig:
                with open(config_path, "w") as file:
                    file.write(str(portConfig))
            return portConfig
    return portConfig


def handle_exit(signum, frame):
    print("Exiting...")
    root.quit()


if __name__ == "__main__":
    drop_privileges()
    subscribe_to_dep()

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    threading.Thread(target=start_tcp_server, daemon=True).start()
    create_gui()
