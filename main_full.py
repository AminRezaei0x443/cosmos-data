import simpy
import json
import random

from cosmos_simulator.roles.blockchain import Blockchain
from cosmos_simulator.roles.relayer import Relayer
from cosmos_simulator.roles.topology_creator import TopologyCreator
from cosmos_simulator.roles.user import User
from cosmos_simulator.simulation import CosmosSimulation
from cosmos_simulator.roles.network_updates import NetworkUpdates


def simulate():
    CosmosSimulation.init()
    env = CosmosSimulation.env

    with open("data/chains-info.json") as f:
        ecosystem = json.load(f)

    chains = {}
    for n in ecosystem["names"]:
        c = Blockchain(env, n, block_time=random.randint(5,10))
        chains[n] = c
        CosmosSimulation.add_chain(c)

    relayer = Relayer(env, list(chains.values()))
    CosmosSimulation.add_relayer(relayer)

    # for n in ecosystem["names"]:
    #     u = User(env, f'user-{n}', n, rate=1)
    #     CosmosSimulation.add_user(u)

    CosmosSimulation.add_user(TopologyCreator(env, chains, ecosystem))
    # CosmosSimulation.add_user(NetworkUpdates(env))

    CosmosSimulation.run(until=4000)

    for chain in chains.values():    
        print(chain.network)
    print(len(ecosystem["conns"]))

if __name__ == "__main__":
    simulate()
