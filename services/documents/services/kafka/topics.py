from enum import StrEnum


class DocumentsKafkaTopic(StrEnum):
    TARIFFS_INBOX = "documents-service.tariffs.inbox"
    RECEIPTS_INBOX = "documents-service.receipts.inbox"
    CONTRACTS_INBOX = "documents-service.contracts.inbox"
