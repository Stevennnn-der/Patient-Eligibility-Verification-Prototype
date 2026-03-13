from datetime import datetime


def is_valid_npi(npi: str) -> bool:
    return npi.isdigit() and len(npi) == 10


def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False