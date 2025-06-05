from enum import StrEnum


class Category(StrEnum):
    FEE = "fee"
    MONEY_IN = "money_in"
    TRANSFER = "transfer"
    BILL_PAYMENT = "bill_payment"
    CASH_WITHDRAWAL = "cash_withdrawal"
    CASHBACK_REWARDS = "cashback_rewards"


def negative_amount(amount: float) -> float:
    return -abs(amount)


def positive_amount(amount: float) -> float:
    return abs(amount)
