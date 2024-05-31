from cosmos_simulator.core.user import User
from cosmos_simulator.core.blockchain import Blockchain
from cosmos_simulator.core.transaction import Transaction
from simpy import Environment


class Relayer(User):
    processed_logs: dict[str, int]

    def __init__(
        self,
        id: str,
        env: Environment,
        chains: dict[str, Blockchain],
        **config,
    ) -> None:
        config["repeat"] = 1
        super().__init__(id, env, chains, **config)
        self.processed_logs = {c.id: 0 for c in chains.values()}

    def act(self):
        while True:
            yield self.env.timeout(1)
            for chain in self.chains.values():
                props = chain.run_method("0x::ls::propagate", "get_propagations")
                last_processed = self.processed_logs[chain.id]
                to_process = props[last_processed:]
                for log in to_process:
                    self.log("process-log", log)
                    target_chain = log.pop("target_chain")
                    target_contract = log.pop("target_contract")
                    tx = Transaction(target_contract, 0, log)
                    self.chains[target_chain].send(tx)
                self.processed_logs[chain.id] = len(props)
