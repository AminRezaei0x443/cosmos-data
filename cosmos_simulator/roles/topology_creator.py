from simpy import Environment
import random

from cosmos_simulator.roles.user import User


class TopologyCreator(User):
    def __init__(self, env: Environment, chains, ecosystem, **config) -> None:
        self.env = env
        self.id = id
        self.sim = None
        self.chains = chains
        self.ecosystem = ecosystem
        self.config = config

    def start(self):
        # yield self.env.timeout(10)
        for src_chain, conn_list in self.ecosystem["conns"].items():
            for dst_chain in conn_list:
                yield self.env.timeout(10)
                self.chains[src_chain].create_connection(dst_chain, "main")
                self.chains[dst_chain].create_connection(src_chain, "main")
