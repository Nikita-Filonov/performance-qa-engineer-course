from enum import StrEnum


class APIRoutes(StrEnum):
    USERS = '/api/v1/users'
    CARDS = '/api/v1/cards'
    TARIFFS = '/api/v1/tariffs'
    PAYMENTS = '/api/v1/payments'
    ACCOUNTS = '/api/v1/accounts'
    CONTRACTS = '/api/v1/contracts'
    DOCUMENTS = '/api/v1/documents'
    OPERATIONS = '/api/v1/operations'

    def as_tag(self) -> str:
        return self.replace('/api/v1/', '')
