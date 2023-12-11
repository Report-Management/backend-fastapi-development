from datetime import datetime, timedelta

def format_relative_time(dateTime):
    now = datetime.now()
    difference = now - dateTime - timedelta(hours=7)

    if difference.total_seconds() < 60:
        return 'just now'
    elif difference.total_seconds() < 3600:
        return f'{int(difference.total_seconds() / 60)} min ago'
    elif difference.total_seconds() < 86400:
        return f'{int(difference.total_seconds() / 3600)} hours ago'
    elif difference.days < 7:
        return f'{difference.days} days ago'
    else:
        return dateTime.strftime("%b %d, %Y %I:%M %p")
