from enum import Enum


class AccountType(str, Enum):
    SAVINGS = "savings"
    CURRENT = "current"


class AccountStatus(str, Enum):
    ACTIVE = "active"
    FROZEN = "frozen"
    CLOSED = "closed"