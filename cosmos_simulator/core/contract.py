from abc import ABC, abstractmethod
from cosmos_simulator.core.transaction import Transaction


class Contract(ABC):
    def __init__(self) -> None: ...

    @abstractmethod
    def state_dict(self): ...

    @abstractmethod
    def load_state_dict(self, state: dict): ...

    @abstractmethod
    def call(self, tx: Transaction): ...
