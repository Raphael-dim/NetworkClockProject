import ctypes
import sys
import datetime


def set_system_time(new_time_str):
    # Parse the new time string
    try:
        new_time = datetime.datetime.strptime(new_time_str, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        print(f"Invalid time format: {e}")
        return

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
        print("Failed to set system time")
    else:
        print("System time successfully set")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: time_setup.py 'YYYY-MM-DD HH:MM:SS'")
        sys.exit(1)

    new_time_str = sys.argv[1]
    set_system_time(new_time_str)
