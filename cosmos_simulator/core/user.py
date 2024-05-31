from abc import ABC, abstractmethod
from cosmos_simulator.core.blockchain import Blockchain
from simpy import Environment


class User(ABC):
    def __init__(
        self, id: str, env: Environment, chains: dict[str, Blockchain], **config
    ) -> None:
        self.env = env
        self.id = id
        self.sim = None
        self.chains = chains
        self.config = config

    @abstractmethod
    def act(self):
        pass

    def start(self):
        repeat = self.config.get("repeat", -1)
        print("Got User", repeat)
        if repeat == -1:
            while True:
                rate = self.config.get("rate", 1)
                yield self.env.timeout(rate)
                self.act()
        else:
            print("Act?", self, self.act)
            yield self.env.process(self.act())
