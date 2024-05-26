import simpy

from cosmos_simulator.roles.blockchain import Blockchain
from cosmos_simulator.roles.relayer import Relayer
from cosmos_simulator.roles.user import User
from cosmos_simulator.simulation import CosmosSimulation
from cosmos_simulator.roles.network_updates import NetworkUpdates


def simulate():
    CosmosSimulation.init()
    env = CosmosSimulation.env

    # Define Blockchains
    A = Blockchain(env, "A", block_time=5)
    B = Blockchain(env, "B", block_time=7)
    C = Blockchain(env, "C", block_time=6)
    
    CosmosSimulation.add_chain(A)
    CosmosSimulation.add_chain(B)
    CosmosSimulation.add_chain(C)

    # Relayer
    relayer = Relayer(env, [A, B, C])
    CosmosSimulation.add_relayer(relayer)

    A.create_connection("B", "main")
    B.create_connection("A", "main")
    B.create_connection("C", "main")
    C.create_connection("B", "main")

    # Users
    user1 = User(env, 'user-a', 'A', rate=1)
    user2 = User(env, 'user-b', 'B', rate=1)
    user3 = User(env, 'user-c', 'C', rate=1)

    CosmosSimulation.add_user(user1)
    CosmosSimulation.add_user(user2)
    CosmosSimulation.add_user(user3)
    CosmosSimulation.add_user(NetworkUpdates(env))

    CosmosSimulation.run(until=40)

    print(A.tx_list)
    print(B.tx_list)
    print(C.tx_list)

    print(A.network)
    print(B.network)
    print(C.network)


if __name__ == "__main__":
    simulate()
