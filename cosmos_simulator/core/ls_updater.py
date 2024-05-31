from cosmos_simulator.core.user import User
from cosmos_simulator.core.blockchain import Blockchain
from cosmos_simulator.core.transaction import Transaction
from simpy import Environment


class LSUpdater(User):
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
        # wait until all chains have connections
        yield self.env.timeout(21000)
        # We connect an empty chain to cosmos hub, to see how propagation works
        src_chain = "cifer1"
        dst_chain = "cosmoshub"
        counterparty_network = self.chains[dst_chain].run_method(
            "0x::ibc", "get_network"
        )
        tx = Transaction(
            "0x::ibc",
            0,
            {
                "method": "connect",
                "chain": dst_chain,
                "updated_network": counterparty_network,
            },
        )
        self.chains[src_chain].send(tx)
