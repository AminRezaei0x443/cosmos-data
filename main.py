import json
import random

from cosmos_simulator.core.blockchain import Blockchain
from cosmos_simulator.core.config import BlockchainConfig
from cosmos_simulator.core.topology_creator import TopologyCreator
from cosmos_simulator.simulation import CosmosSimulation
from cosmos_simulator.core.ibc import IBC
from cosmos_simulator.util.log import log


def simulate():
    CosmosSimulation.init()
    env = CosmosSimulation.env

    with open("data/chains-info.json") as f:
        ecosystem = json.load(f)

    chains = {}
    for n in ecosystem["names"]:
        cfg = BlockchainConfig(block_time=random.randint(5, 10))
        c = Blockchain(n, env, cfg)
        ibc = IBC()
        c.deploy("0x::ibc", ibc, precompile=True)
        chains[n] = c
        CosmosSimulation.add_chain(c)

    CosmosSimulation.add_user(
        TopologyCreator("relayer:topology-creator", env, chains, ecosystem)
    )
    CosmosSimulation.run(until=4000)

    log("app", "main", "sim-done", env.now, "Simulation Done")
    cs = 0
    for chain in chains.values():
        r = chain.run_method("0x::ibc", "get_connections")
        log("app", chain.id, "analytics", env.now, f"connections: {r}")
        cs += len(r)
    log("app", "main", "analytics", env.now, f"connections num: {cs}")


if __name__ == "__main__":
    simulate()
