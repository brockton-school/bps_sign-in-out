def format_time(datetime_obj):
    """Formats a datetime object into a 12-hour time string."""
    return datetime_obj.strftime('%I:%M %p')
