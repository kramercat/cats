from datetime import datetime
from zoneinfo import ZoneInfo


datetime_format = "%Y-%m-%d %H:%M:%S"


def now() -> datetime:
    """
    Return the current datetime.
    """
    return datetime.now(tz=ZoneInfo("UTC"))


def format_date(datetime_obj: datetime) -> str:
    """
    Parse a datetime into a formatted string.
    """
    return datetime_obj.strftime(datetime_format)


def parse_date(date_str: str) -> datetime:
    """
    Parse a date string in 'YYYY-MM-DD HH:MM:SS' format to a datetime object.
    """
    return datetime.strptime(date_str, datetime_format)


def to_timestamp(date_str: str) -> int:
    """
    Convert a date string (in 'YYYY-MM-DD HH:MM:SS' format) to a Unix timestamp.
    """
    return int(parse_date(date_str).timestamp())
