import datetime


def get_formatted_time(format_string="%Y-%m-%d %H:%M:%S"):
    now = datetime.datetime.now()
    try:
        return now.strftime(format_string)
    except Exception as e:
        return f"Error formatting time: {e}"


def set_system_time(new_time):
    # Placeholder for setting system time - actual implementation will require administrative privileges
    raise NotImplementedError("Setting system time requires elevated privileges")


if __name__ == "__main__":
    print(get_formatted_time())
