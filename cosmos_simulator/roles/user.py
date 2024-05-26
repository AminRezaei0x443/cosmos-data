from simpy import Environment


class User:
    def __init__(self, env: Environment, id: str, chain: str, **config) -> None:
        self.env = env
        self.id = id
        self.sim = None
        self.chain = chain
        self.config = config

    def start(self):
        while True:
            rate = self.config.get("rate", 1)
            yield self.env.timeout(rate)

            target_chain = self.config.get("target_chain", None)
            src = self.sim.chains[self.chain]
            if target_chain:
                src.cross_chain_invoke(target_chain, 'addr', b'')
            else:
                src.invoke('addr', b'')

