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

    def log(self, event: str, message: str):
        log("user", self.id, event, self.env.now, message)

    def start(self):
        repeat = self.config.get("repeat", -1)
        self.log("user-boot", f"Booting user with repeat: {repeat}")
        if repeat == -1:
            while True:
                rate = self.config.get("rate", 1)
                yield self.env.timeout(rate)
                normal = self.config.get("normal", False)
                if normal:
                    self.act()
                else:
                    yield self.env.process(self.safe_act())
        else:
            yield self.env.process(self.safe_act())
