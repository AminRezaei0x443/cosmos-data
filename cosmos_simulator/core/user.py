import types
from abc import ABC, abstractmethod
from cosmos_simulator.core.blockchain import Blockchain
from simpy import Environment

from cosmos_simulator.util.log import log


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

    def safe_act(self):
        action = self.act()
        if isinstance(action, types.GeneratorType):
            yield self.env.process(action)
        else:
            yield action

    def start(self):
        repeat = self.config.get("repeat", -1)
        log(
            "user",
            self.id,
            "user-boot",
            self.env.now,
            f"Booting user with repeat: {repeat}",
        )
        if repeat == -1:
            while True:
                rate = self.config.get("rate", 1)
                yield self.env.timeout(rate)
                yield self.env.process(self.safe_act())
        else:
            yield self.env.process(self.safe_act())
