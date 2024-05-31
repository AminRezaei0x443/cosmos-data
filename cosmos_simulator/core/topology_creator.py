from cosmos_simulator.core.user import User
from cosmos_simulator.core.blockchain import Blockchain
from cosmos_simulator.core.transaction import Transaction
from simpy import Environment


class TopologyCreator(User):
    def __init__(
        self,
        id: str,
        env: Environment,
        chains: dict[str, Blockchain],
        ecosystem: dict,
        **config,
    ) -> None:
        # we have custom yields
        config["repeat"] = 1
        super().__init__(id, env, chains, **config)
        self.ecosystem = ecosystem

    def act(self):
        tc = 0
        for src_chain, conn_list in self.ecosystem["conns"].items():
            tc += len(conn_list)
        self.log("creating-connections", f"num links: {tc // 2}")

        for src_chain, conn_list in self.ecosystem["conns"].items():
            for dst_chain in conn_list:
                yield self.env.timeout(1)
                tx = Transaction(
                    "0x::ibc", 0, {"method": "connect", "chain": dst_chain}
                )
                self.chains[src_chain].send(tx)
