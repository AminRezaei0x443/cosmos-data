from cosmos_simulator.core.contract import Contract
from cosmos_simulator.core.transaction import Transaction, TransactionState


class IBC(Contract):
    connections: list[str]

    def __init__(self):
        super().__init__()
        self.connections = []

    def connect(self, chain: str = None, **kwargs) -> None:
        if chain is None:
            raise ValueError("Chain cannot be None")
        self.connections.append(chain)

    def disconnect(self, chain: str = None, **kwargs) -> None:
        if chain is None:
            raise ValueError("Chain cannot be None")
        if chain not in self.connections:
            raise ValueError("Chain is not connected")
        self.connections.remove(chain)

    def state_dict(self):
        return {
            "connections": self.connections,
        }

    def load_state_dict(self, state: dict):
        self.connections = state.get("connections", [])

    def call(self, tx: Transaction):
        method = tx.data.pop("method", None)
        if method is None:
            raise ValueError("Method cannot be None")
        if method == "connect":
            self.connect(**tx.data)
        elif method == "disconnect":
            self.disconnect(**tx.data)
        else:
            raise ValueError("Method is not supported")

    def get_method(self, method: str, **params):
        if method == "get_connections":
            return self.connections
