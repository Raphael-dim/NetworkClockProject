def validate_format_string(format_string):
    try:
        formatted = format_string.format(
            year=2020, month=1, day=1, hour=0, minute=0, second=0
        )
        return True, formatted
    except Exception as e:
        return False, f"Invalid format string: {e}"


if __name__ == "__main__":
    format_string = "%Y-%m-%d %H:%M:%S"
    is_valid, message = validate_format_string(format_string)
    if is_valid:
        print(f"Valid format string: {message}")
    else:
        print(f"Error: {message}")
