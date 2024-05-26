from simpy import Environment
from cosmos_simulator.roles.blockchain import Blockchain


class Relayer:
    def __init__(self, env: Environment, chains: list[Blockchain]):
        self.env = env
        self.chains = chains
        self.sim = None
        self.last_processed_height = {c.id: 0 for c in chains}

    def start(self):
        print("Relayer Started:", self.env.now)
        while True:
            print("Relayer Working:", self.env.now)
            for c in self.chains:
                last_processed_height = self.last_processed_height[c.id]
                unprocessed_tx = c.tx_list[last_processed_height:]
                print(c, last_processed_height)
                for tx in unprocessed_tx:
                    print(tx)
                    target = tx.get("target", None)
                    if target:
                        tc = self.sim.get_chain(target)
                        tt = tx.get("type", None)
                        if tt == "ack":
                            tc.relay_ack(tx)
                        elif tt == "cross_chain" or tt == "link-state-propagation":
                            print("relaying...", tx)
                            tc.relay_target(c.id, tx)
                self.last_processed_height[c.id] += len(unprocessed_tx)
            yield self.env.timeout(1)

