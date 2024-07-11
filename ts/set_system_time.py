import os
import sys
import datetime

date_str = sys.argv[1]
time_str = sys.argv[2]

try:
    new_time = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
except ValueError as e:
    print(f"Invalid time format: {e}")
    sys.exit(1)

if os.name == "nt":  # Windows
    import ctypes

    SYSTEMTIME = ctypes.c_uint16 * 8
    st = SYSTEMTIME(
        new_time.year,
        new_time.month,
        new_time.weekday(),
        new_time.day,
        new_time.hour,
        new_time.minute,
        new_time.second,
        0,
    )

    SetLocalTime = ctypes.windll.kernel32.SetLocalTime
    SetLocalTime.argtypes = [ctypes.POINTER(SYSTEMTIME)]
    SetLocalTime.restype = ctypes.c_bool
    if not SetLocalTime(ctypes.byref(st)):
        raise ctypes.WinError()
