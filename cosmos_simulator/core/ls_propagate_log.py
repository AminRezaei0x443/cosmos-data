import typing

from cosmos_simulator.core.contract import Contract
from cosmos_simulator.core.transaction import Transaction


if typing.TYPE_CHECKING:
    from cosmos_simulator.core.blockchain import Blockchain


class LSLogPropagate(Contract):
    propagations: list[dict]

    def __init__(self, chain: "Blockchain"):
        super().__init__(chain)
        self.propagations = []

    def state_dict(self):
        return {
            "propagations": self.propagations,
        }

    def load_state_dict(self, state: dict):
        self.propagations = state.get("propagations", [])

    def call(self, tx: Transaction):
        method = tx.data.get("method", None)
        if method == "ls_update":
            self.propagations.append(tx.data)
            return
        raise ValueError("Method is not supported")

    def get_method(self, method: str, **params):
        if method == "get_propagations":
            return self.propagations
        raise ValueError("Method is not supported")
