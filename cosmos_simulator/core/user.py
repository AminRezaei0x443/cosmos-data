from abc import ABC, abstractmethod
from cosmos_simulator.core.blockchain import Blockchain
from simpy import Environment


class User(ABC):
    def __init__(
        self, env: Environment, id: str, chains: list[Blockchain], **config
    ) -> None:
        self.env = env
        self.id = id
        self.sim = None
        self.chains = {chain.id: chain for chain in chains}
        self.config = config

    @abstractmethod
    def act(self):
        pass

    def start(self):
        while True:
            rate = self.config.get("rate", 1)
            yield self.env.timeout(rate)

            self.act()
