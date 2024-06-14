import typing
import uuid

from cosmos_simulator.core.ibc import IBC
from networkx import Graph, compose

from cosmos_simulator.core.transaction import Transaction

if typing.TYPE_CHECKING:
    from cosmos_simulator.core.blockchain import Blockchain


class LinkStateIBC(IBC):
    network: Graph
    processed_updates: list[str]

    def __init__(self, chain: "Blockchain"):
        super().__init__(chain)
        self.network = Graph()
        self.processed_updates = []

    def connect(self, chain: str = None, **kwargs) -> None:
        super().connect(chain=chain, **kwargs)
        updated_network = kwargs.get("updated_network", Graph())
        self.network = compose(self.network, updated_network)
        self.network.add_edge(self.chain.id, chain)
        # Let the network know about updates
        update_id = uuid.uuid4().hex
        #
        for c in self.connections:
            tx = Transaction(
                "0x::ls::propagate",
                0,
                {
                    "method": "ls_update",
                    "update_id": update_id,
                    "target_chain": c,
                    "target_contract": "0x::ibc",
                    "updated_network": self.network,
                },
            )
            self.chain.send(tx)

    def disconnect(self, chain: str = None, **kwargs) -> None:
        super().disconnect(chain=chain, **kwargs)
        self.network.remove_edge(self.chain.id, chain)
        # Let the network know about updates
        update_id = uuid.uuid4().hex
        for c in self.connections:
            tx = Transaction(
                "0x::ls::propagate",
                0,
                {
                    "method": "ls_update",
                    "update_id": update_id,
                    "target_chain": c,
                    "target_contract": "0x::ibc",
                    "updated_network": self.network,
                    "deleted_links": [(self.chain.id, c)],
                },
            )
            self.chain.send(tx)

    def ls_update(self, **kwargs) -> None:
        # Check update id
        update_id: str | None = kwargs.get("update_id", None)
        if update_id is None:
            raise ValueError("update_id is required")
        if update_id in self.processed_updates:
            return
        # 1. Do a graph sync
        updated_network = kwargs.get("updated_network", Graph())
        new_net = compose(self.network, updated_network)
        # 2. Do a diff
        deleted_links = kwargs.get("deleted_links", [])
        for s, d in deleted_links:
            new_net.remove_edge(s, d)
        self.network = new_net
        self.processed_updates.append(update_id)
        # 3. Propagate to others
        source_chain = kwargs.pop("source_chain", None)
        for c in self.connections:
            if c == source_chain:
                continue
            tx = Transaction(
                "0x::ls::propagate",
                0,
                {
                    **kwargs,
                    "target_chain": c,
                    "target_contract": "0x::ibc",
                    "updated_network": self.network,
                    "deleted_links": [(self.chain.id, c)],
                },
            )
            self.chain.send(tx)
        print("update ibc")

    def state_dict(self):
        return {
            **super().state_dict(),
            "network": self.network,
        }

    def load_state_dict(self, state_dict: dict):
        super().load_state_dict(state_dict)
        self.network = state_dict.get("network", Graph())

    def call(self, tx: Transaction):
        method = tx.data.get("method", None)
        if method == "ls_update":
            self.ls_update(**tx.data)
            return
        super().call(tx)

    def get_method(self, method: str, **params):
        if method == "get_network":
            return self.network
        return super().get_method(method, **params)
