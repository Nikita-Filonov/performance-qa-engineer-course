from datetime import date, timedelta


def build_card_holder(first_name: str, last_name: str) -> str:
    return f"{first_name} {last_name}"


def build_card_expired_at() -> date:
    return date.today() + timedelta(days=365 * 7)
