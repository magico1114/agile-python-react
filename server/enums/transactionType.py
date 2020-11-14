from enum import Enum

class transactionType(str, Enum):
    CREDIT = 'credit'
    DEBIT = 'debit'

    def __str__(self):
        return str(self.value)