from datetime import datetime, timedelta


def parse_date(date_str: str, fmt: str = "%Y-%m-%d") -> datetime:
    """
    Convert a date string into a datetime object.

    Example:
        parse_date("2026-01-20")
    """
    return datetime.strptime(date_str, fmt)


def days_ago(days: int) -> datetime:
    """
    Return a datetime representing N days ago from now.

    Example:
        days_ago(7)
    """
    return datetime.now() - timedelta(days=days)


def is_within_last_days(date_str: str, days: int) -> bool:
    """
    Check if the given date string is within the last N days.

    Example:
        is_within_last_days("2026-01-18", 7)
    """
    date = parse_date(date_str)
    return date >= days_ago(days)


def format_date(date: datetime, fmt: str = "%Y-%m-%d") -> str:
    """
    Format a datetime object as a string.
    """
    return date.strftime(fmt)
