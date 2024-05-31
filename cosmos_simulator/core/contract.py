import typing
from abc import ABC, abstractmethod
from cosmos_simulator.core.transaction import Transaction

if typing.TYPE_CHECKING:
    from cosmos_simulator.core.blockchain import Blockchain


class Contract(ABC):
    chain: "Blockchain"

    def __init__(self, blockchain: "Blockchain") -> None:
        self.chain = blockchain

    @abstractmethod
    def state_dict(self): ...

    @abstractmethod
    def load_state_dict(self, state: dict): ...

    @abstractmethod
    def call(self, tx: Transaction): ...

    @abstractmethod
    def get_method(self, method: str, **params): ...
