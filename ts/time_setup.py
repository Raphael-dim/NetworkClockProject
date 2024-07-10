import ctypes
import datetime
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

# Default format
default_format = "%Y-%m-%d %H:%M:%S"

# Global variable for current format
current_format = default_format


def set_system_time(new_time):
    # Define SYSTEMTIME structure
    class SYSTEMTIME(ctypes.Structure):
        _fields_ = [
            ("wYear", ctypes.c_short),
            ("wMonth", ctypes.c_short),
            ("wDayOfWeek", ctypes.c_short),
            ("wDay", ctypes.c_short),
            ("wHour", ctypes.c_short),
            ("wMinute", ctypes.c_short),
            ("wSecond", ctypes.c_short),
            ("wMilliseconds", ctypes.c_short),
        ]

    system_time = SYSTEMTIME(
        wYear=new_time.year,
        wMonth=new_time.month,
        wDayOfWeek=new_time.weekday(),
        wDay=new_time.day,
        wHour=new_time.hour,
        wMinute=new_time.minute,
        wSecond=new_time.second,
        wMilliseconds=int(new_time.microsecond / 1000),
    )

    # Set system time using Windows API
    if not ctypes.windll.kernel32.SetSystemTime(ctypes.byref(system_time)):
        messagebox.showerror("Error", "Failed to set system time")
    else:
        messagebox.showinfo("Success", "System time successfully set")
        update_label_time()  # Update displayed time in the main application


root = tk.Tk()
time_label = tk.Label(root, text="", font=("Courier", 24), fg="white", bg="black")


def update_label_time():
    current_time = datetime.datetime.now().strftime(current_format)
    time_label.config(text=current_time)


def create_gui():

    def edit_date_time():
        selected_date = cal.get_date()
        selected_time = datetime.time(
            int(hour_var.get()), int(minute_var.get()), int(second_var.get())
        )
        new_time = datetime.datetime.combine(selected_date, selected_time)
        set_system_time(new_time)

    def update_format():
        global current_format
        new_format = format_entry.get()
        try:
            datetime.datetime.now().strftime(new_format)  # Check if format is valid
            current_format = new_format
            update_label_time()
        except ValueError:
            messagebox.showerror("Error", "Invalid format specified")

    def reset_format():
        global current_format
        current_format = default_format
        format_entry.delete(0, tk.END)  # Clear the entry
        format_entry.insert(0, default_format)  # Insert default format
        update_label_time()

    root.title("Set System Time")
    root.configure(background="black")
    root.geometry("500x500")  # Adjust main window size

    time_label.pack(pady=20)

    edit_format_frame = tk.Frame(
        root,
        bg="black",
        bd=0,
        relief=tk.SOLID,
        highlightbackground="white",
        highlightthickness=2,
    )  # Edit frame

    edit_format_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    # New widgets for format editing
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
    format_entry.insert(0, default_format)  # Default format

    update_button = tk.Button(
        edit_format_frame, text="Update Format", command=update_format
    )
    update_button.pack(pady=10)
    reset_button = tk.Button(edit_format_frame, text="Reset", command=reset_format)
    reset_button.pack(pady=10,  padx=10)

    edit_frame = tk.Frame(
        root,
        bg="black",
        bd=0,
        relief=tk.SOLID,
        highlightbackground="white",
        highlightthickness=2,
    )  # Edit frame

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

    update_label_time()  # Update displayed time on application start

    def update_time():
        update_label_time()
        root.after(1000, update_time)

    update_time()

    root.mainloop()


if __name__ == "__main__":
    # Open GUI window
    create_gui()
