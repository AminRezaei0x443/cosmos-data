from cosmos_simulator.core.user import User
from cosmos_simulator.core.blockchain import Blockchain
from cosmos_simulator.core.transaction import Transaction
from simpy import Environment


class TopologyCreator(User):
    def __init__(
        self,
        env: Environment,
        id: str,
        chains: list[Blockchain],
        ecosystem: dict,
        **config
    ) -> None:
        # we have custom yields
        config["rate"] = 0
        super().__init__(env, id, chains, **config)
        self.ecosystem = ecosystem

    def act(self):
        for src_chain, conn_list in self.ecosystem["conns"].items():
            for dst_chain in conn_list:
                yield self.env.timeout(10)
                tx = Transaction(
                    "0x::ibc", 0, {"method": "connect", "chain": dst_chain}
                )
                self.chains[src_chain].send(tx)
                tx2 = Transaction(
                    "0x::ibc", 0, {"method": "connect", "chain": src_chain}
                )
                self.chains[dst_chain].send(tx2)
