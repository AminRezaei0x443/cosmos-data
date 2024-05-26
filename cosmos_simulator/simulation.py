import simpy
from cosmos_simulator.roles.blockchain import Blockchain
from cosmos_simulator.roles.relayer import Relayer
from cosmos_simulator.roles.user import User


class CosmosSimulation:
    env: simpy.Environment
    chains: dict[str, Blockchain]
    relayers: list[Relayer]
    users: list[User]

    @classmethod
    def init(cls):
        cls.env = simpy.Environment()
        cls.chains = {}
        cls.users = []
        cls.relayers = []
    
    @classmethod
    def add_chain(cls, blockchain: Blockchain):
        cls.chains[blockchain.id] = blockchain

    @classmethod
    def add_relayer(cls, relayer: Relayer):
        relayer.sim = cls
        cls.relayers.append(relayer)
    
    @classmethod
    def add_user(cls, user: User):
        user.sim = cls
        cls.users.append(user)
    
    @classmethod
    def get_chain(cls, name: str) -> Blockchain:
        return cls.chains[name]
    
    @classmethod
    def run(cls, until=10):
        for blockchain in cls.chains.values():
            cls.env.process(blockchain.start())
        for relayer in cls.relayers:
            cls.env.process(relayer.start())
        for user in cls.users:
            cls.env.process(user.start())
        cls.env.run(until=until)
