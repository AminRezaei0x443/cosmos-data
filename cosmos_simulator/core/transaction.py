from enum import IntEnum


class TransactionState(IntEnum):
    DRAFT = 0
    ACCEPTED = 1
    REJECTED = 2
    DONE = 3


Action = dict


class Transaction:
    state: TransactionState
    # base info
    target: str
    value: int
    data: dict
    # exec info
    gas_used: int
    out_actions: list[Action]
    time: int
    block: int

    def __init__(self, target: str, value: int, data: dict):
        self.target = target
        self.value = value
        self.data = data
        self.state = TransactionState.DRAFT
        self.gas_used = 0
        self.out_actions = []
        self.time = 0
        self.block = 0
