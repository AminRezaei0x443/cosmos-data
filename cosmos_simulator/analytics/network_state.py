from networkx import Graph
from simpy import Environment

from cosmos_simulator.core.blockchain import Blockchain
from cosmos_simulator.core.user import User


class NetworkStateChecker(User):
    def __init__(
        self,
        id: str,
        env: Environment,
        chains: dict[str, Blockchain],
        link: tuple[str],
        **config,
    ):
        config["normal"] = True
        config["repeat"] = -1
        config["rate"] = 1
        super().__init__(id, env, chains, **config)
        self.link = link

    def act(self):
        N = 0
        U = 0
        u, v = self.link
        for chain in self.chains.values():
            n: Graph = chain.run_method("0x::ibc", "get_network")
            N += 1
            if n.has_edge(u, v):
                U += 1
        self.log("net-update", f"{U/N}")
