from datetime import date, datetime


def to_proto_date(value: date) -> str:
    return value.strftime('%d-%m-%Y')


def from_proto_date(value: str) -> date:
    return datetime.strptime(value, "%d-%m-%Y").date()


def to_proto_datetime(value: datetime) -> str:
    return value.strftime('%d-%m-%Y %H:%M:%S')


def from_proto_datetime(value: str) -> datetime:
    return datetime.strptime(value, "%d-%m-%Y %H:%M:%S")
