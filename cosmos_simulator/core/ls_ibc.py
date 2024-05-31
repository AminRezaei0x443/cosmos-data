import typing

from cosmos_simulator.core.ibc import IBC
from networkx import Graph, compose


if typing.TYPE_CHECKING:
    from cosmos_simulator.core.blockchain import Blockchain


class LinkStateIBC(IBC):
    network: Graph

    def __init__(self, chain: "Blockchain"):
        super().__init__(chain)
        self.network = Graph()

    def connect(self, chain: str = None, **kwargs) -> None:
        super().connect(chain=chain, **kwargs)
        updated_network = kwargs.get("updated_network", Graph())
        self.network = compose(self.network, updated_network)
        self.network.add_edge(self.chain.id, chain)

    def disconnect(self, chain: str = None, **kwargs) -> None:
        super().disconnect(chain=chain, **kwargs)
        self.network.remove_edge(self.chain.id, chain)

    def state_dict(self):
        return {
            **super().state_dict(),
            "network": self.network,
        }

    def load_state_dict(self, state_dict: dict):
        super().load_state_dict(state_dict)
        self.network = state_dict.get("network", Graph())

    def get_method(self, method: str, **params):
        if method == "get_network":
            return self.network
        return super().get_method(method, **params)
