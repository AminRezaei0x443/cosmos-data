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
from networkx import Graph, diameter


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
    print(diameter(network))


if __name__ == "__main__":
    simulate()
