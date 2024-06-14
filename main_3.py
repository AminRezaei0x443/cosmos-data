import json
import random

from cosmos_simulator.analytics.network_state import NetworkStateChecker
from cosmos_simulator.core.blockchain import Blockchain
from cosmos_simulator.core.config import BlockchainConfig
from cosmos_simulator.core.ls_topology_creator import LSTopologyCreator
from cosmos_simulator.core.relayer import Relayer
from cosmos_simulator.simulation import CosmosSimulation
from cosmos_simulator.core.ls_ibc import LinkStateIBC
from cosmos_simulator.core.ls_updater import LSUpdater
from cosmos_simulator.core.ls_propagate_log import LSLogPropagate
from cosmos_simulator.util.log import log
from networkx import Graph


def simulate():
    # Init Sim Environment
    CosmosSimulation.init()
    env = CosmosSimulation.env

    # Load Real Network Data
    with open("data/chains-info.json") as f:
        ecosystem = json.load(f)

    network = Graph()
    for src_chain, conns in ecosystem["conns"].items():
        for dst_chain in conns:
            network.add_edge(src_chain, dst_chain)
    print("initial network", network)

    chains = {}
    for n in ecosystem["names"]:
        # Create Chains
        cfg = BlockchainConfig(block_time=random.randint(10, 20))
        c = Blockchain(n, env, cfg)
        # Precompile Contracts
        ibc = LinkStateIBC(c)
        ibc.connections = ecosystem["conns"].get(n, [])
        ibc.network = network
        c.deploy("0x::ibc", ibc, precompile=True)
        prop = LSLogPropagate(c)
        c.deploy("0x::ls::propagate", prop, precompile=True)
        # Define Chains
        chains[n] = c
        CosmosSimulation.add_chain(c)

    # Add the user responsible for creating topologies
    # CosmosSimulation.add_user(
    #     LSTopologyCreator("relayer:topology-creator", env, chains, ecosystem)
    # )

    CosmosSimulation.add_user(LSUpdater("relayer:link-up-1", env, chains, ecosystem))
    CosmosSimulation.add_user(Relayer("relayer:propagator", env, chains))
    CosmosSimulation.add_user(
        NetworkStateChecker("stats:checker", env, chains, ["cifer1", "cosmoshub"])
    )
    # Run the simulation
    CosmosSimulation.run(until=60000)
    log("app", "main", "sim-done", env.now, "Simulation Done")

    # Check the actual connections
    cs = 0

    for chain in chains.values():
        r = chain.run_method("0x::ibc", "get_connections")
        n = chain.run_method("0x::ibc", "get_network")
        cs += len(r)
        # log("app", chain.id, "analytics", env.now, f"connections: {r}")
        log("app", chain.id, "analytics", env.now, f"network: {n}")

    log("app", "main", "analytics", env.now, f"num links: {cs // 2}")


if __name__ == "__main__":
    simulate()
