"""Natural language date parsing utility."""

import re
from datetime import datetime, timedelta


def parse_natural_date(date_str: str) -> datetime | None:
    """Parse natural language date strings into datetime objects.

    Supported formats:
    - YYYY-MM-DD (also accepts YYYY-M-D)
    - tomorrow
    - today
    - next [day]
    - in [X] days

    Args:
        date_str: The string to parse.

    Returns:
        The parsed datetime object, or None if parsing fails.
    """
    date_str = date_str.lower().strip()
    if not date_str:
        return None

    # Helper function to parse a single segment
    def _parse_segment(seg: str) -> datetime | None:
        seg = seg.strip()
        if not seg:
            return None

        # Try flexible ISO-ish format (YYYY-MM-DD or YYYY-M-D)
        # Check this FIRST because it's more specific than "today"
        match = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", seg)
        if match:
            try:
                return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            except ValueError:
                return None

        # today
        if seg == "today":
            now = datetime.now()
            return now.replace(hour=0, minute=0, second=0, microsecond=0)

        # tomorrow
        if seg == "tomorrow":
            now = datetime.now()
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
            return today + timedelta(days=1)

        # next [day]
        days_of_week = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6,
        }
        match = re.match(r"^next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)$", seg)
        if match:
            now = datetime.now()
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
            target_day = days_of_week[match.group(1)]
            current_day = today.weekday()
            days_ahead = target_day - current_day
            if days_ahead <= 0:
                days_ahead += 7
            return today + timedelta(days=days_ahead)

        # in [X] days
        match = re.match(r"^in\s+(\d+)\s+days?$", seg)
        if match:
            now = datetime.now()
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
            return today + timedelta(days=int(match.group(1)))

        return None

    # 1. Try parsing the WHOLE string first (in case it's "next monday")
    result = _parse_segment(date_str)
    if result:
        return result

    # 2. If it contains commas, try segments.
    # If the user typed "today, 2027-12-2", we want the more specific one (usually the date format).
    if "," in date_str:
        segments = date_str.split(",")
        parsed_segments = [res for seg in segments if (res := _parse_segment(seg))]

        if parsed_segments:
            # Prefer specifically formatted dates (YYYY-MM-DD) over "today"/"tomorrow"
            # If any segment matched a date regex, it's already a datetime.
            # We'll just return the LAST valid parsed segment, assuming it's the more specific one.
            return parsed_segments[-1]

    return None


