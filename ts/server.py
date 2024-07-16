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
    """Convert user-friendly date/time format to strftime-compatible format."""
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
    """Drop unnecessary privileges."""
    try:
        # On UNIX-like systems, drop root privileges if we have them
        if os.name != "nt" and os.getuid() == 0:
            os.setuid(os.geteuid())
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
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(5)
    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


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
