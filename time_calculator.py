"""
Adds the given duration time to the start time and returns the result.
"""


def add_time(start_time, duration, starting_day=None):
    """
    Adds the given duration time to the start time and returns the result.

    Args:
        start_time (str):
            The start time in the format 'HH:MM AM/PM'.
        duration (str):
            The duration to add in the format 'HH:MM'.
        starting_day (str, optional):
            The starting day of the week. Defaults to None.

    Returns:
        str: The resulting time after adding the duration.
    """
    # Constants
    hours_in_day = 24
    minutes_in_hour = 60

    # Parse the start time and duration
    start_hour, start_minute, period = parse_start_time(start_time)
    duration_hour, duration_minute = parse_duration(duration)

    # Adjust time if PM
    if period == "PM":
        start_hour += 12

    # Calculate the total minutes
    total_minutes = start_hour * minutes_in_hour + start_minute + \
        duration_hour * minutes_in_hour + duration_minute

    # Calculate the total hours and days
    total_hours = total_minutes // minutes_in_hour
    total_days = total_hours // hours_in_day

    # Calculate the final hour and period
    final_hour = total_hours % hours_in_day % 12
    if final_hour == 0:
        final_hour = 12

    period = "AM" if total_hours % hours_in_day <= 11 else "PM"

    # Determine the final day of the week
    final_day = None
    if starting_day:
        starting_day = starting_day.lower()
        days_of_week = ["sunday", "monday", "tuesday",
                        "wednesday", "thursday", "friday", "saturday"]
        final_day_index = (days_of_week.index(starting_day) + total_days) % 7
        final_day = days_of_week[final_day_index].capitalize()

    # Generate the time string
    time_string = f"{final_hour}:{format_min(total_minutes % minutes_in_hour)} {period}"

    if final_day:
        if total_days == 0:
            return f"{time_string}, {final_day}"
        if total_days == 1:
            return f"{time_string}, {final_day} (next day)"
        return f"{time_string}, {final_day} ({total_days} days later)"

    if total_days == 1:
        return f"{time_string} (next day)"
    if total_days > 1:
        return f"{time_string} ({total_days} days later)"

    return time_string


def parse_start_time(start_time):
    """
    Parse the start time string into hour, minute, and period.

    Args:
        start_time (str): The start time in the format 'HH:MM AM/PM'.

    Returns:
        tuple: A tuple containing hour, minute, and period.
    """
    time, period = start_time.split(" ")
    hour, minute = time.split(":")
    return int(hour), int(minute), period.upper()


def parse_duration(duration):
    """
    Parse the duration string into hour and minute.

    Args:
        duration (str): The duration to add in the format 'HH:MM'.

    Returns:
        tuple: A tuple containing hour and minute.
    """
    hour, minute = duration.split(":")
    return int(hour), int(minute)


def format_min(minute):
    """
    Format the minute value to include leading zero if less than 10.

    Args:
        minute (int): The minute value.

    Returns:
        str: Formatted minute value as a string.
    """
    return f"0{minute}" if minute < 10 else str(minute)
