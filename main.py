import json
import random

from cosmos_simulator.core.blockchain import Blockchain
from cosmos_simulator.core.config import BlockchainConfig
from cosmos_simulator.core.topology_creator import TopologyCreator
from cosmos_simulator.simulation import CosmosSimulation
from cosmos_simulator.core.ibc import IBC
from cosmos_simulator.util.log import log


def simulate():
    # Init Sim Environment
    CosmosSimulation.init()
    env = CosmosSimulation.env

    # Load Real Network Data
    with open("data/chains-info.json") as f:
        ecosystem = json.load(f)

    chains = {}
    for n in ecosystem["names"]:
        # Create Chains
        cfg = BlockchainConfig(block_time=random.randint(5, 10))
        c = Blockchain(n, env, cfg)
        # Precompile Contracts
        ibc = IBC()
        c.deploy("0x::ibc", ibc, precompile=True)
        # Define Chains
        chains[n] = c
        CosmosSimulation.add_chain(c)

    # Add the user responsible for creating topologies
    CosmosSimulation.add_user(
        TopologyCreator("relayer:topology-creator", env, chains, ecosystem)
    )

    # Run the simulation
    CosmosSimulation.run(until=4000)
    log("app", "main", "sim-done", env.now, "Simulation Done")

    # Check the actual connections
    cs = 0

    for chain in chains.values():
        r = chain.run_method("0x::ibc", "get_connections")
        cs += len(r)
        log("app", chain.id, "analytics", env.now, f"connections: {r}")

    log("app", "main", "analytics", env.now, f"num links: {cs // 2}")


if __name__ == "__main__":
    simulate()
