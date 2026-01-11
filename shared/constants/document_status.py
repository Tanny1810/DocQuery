from enum import IntEnum


class DocumentStatus(IntEnum):
    UPLOADED = 1
    QUEUED = 2
    PROCESSING = 3
    RETRYING = 4
    PARTIAL = 5
    READY = 6
    CANCELLED = 7
    FAILED = 8
    DELETED = 9
