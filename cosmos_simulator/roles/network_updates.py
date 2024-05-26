from simpy import Environment
import random

from cosmos_simulator.roles.user import User


class NetworkUpdates(User):
    def __init__(self, env: Environment, **config) -> None:
        self.env = env
        self.id = id
        self.sim = None
        self.config = config

    def start(self):
        while True:
            rate = self.config.get("rate", 1)
            yield self.env.timeout(rate)

            f = list(self.sim.chains.keys())
            c_id = random.randint(0, len(f) - 1)
            picked = f[c_id]
            src = self.sim.chains[picked]
            src.update_connection()
