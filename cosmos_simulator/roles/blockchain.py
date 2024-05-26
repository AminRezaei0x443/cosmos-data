from simpy import Environment
from networkx import Graph, compose


class Blockchain:
    tx_hash = 0

    def __init__(self, env: Environment, id: str, **config) -> None:
        self.env = env
        self.id = id
        self.config = config
        self.mempool = []
        self.connections = []
        self.tx_list = []
        self.block_seq = 0
        self.tx_hash = 0
        self.network = Graph()

    def submit_tx(self, tx: dict):
        Blockchain.tx_hash += 1
        self.mempool.append({"hash": Blockchain.tx_hash, **tx})

    # user
    def invoke(self, addr: str, data: bytes):
        self.submit_tx({"type": "invoke", "addr": addr, "data": data})

    # user
    def cross_chain_invoke(self, target_chain: str, addr: str, data: bytes):
        self.submit_tx(
            {"type": "cross_chain", "target": target_chain, "addr": addr, "data": data}
        )

    # relayer
    def update_client(self, for_chain: str, data: bytes):
        self.submit_tx({"type": "update_client", "target": for_chain, "data": data})

    # relayer
    def create_connection(self, target_chain: str, chan: str):
        self.submit_tx({"type": "create-client", "target": target_chain})
        self.submit_tx({"type": "create-channel", "channel": chan})
        for c in self.connections:
            self.submit_tx(
                {
                    "type": "link-state-propagation",
                    "target": c,
                    "call-stack": [self.id],
                    "connection_changes": {f"{self.id}-{target_chain}": "NEW"},
                    "network_state": self.network,
                }
            )
        self.connections.append(target_chain)

    # relayer
    def update_connection(self):
        for c in self.connections:
            self.submit_tx(
                {"type": "link-state-propagation", "target": c, "call-stack": [self.id], "network_state": self.network}
            )

    # relayer
    def relay_target(self, from_: str, tx: dict, update_client=True):
        if update_client and tx.get("target", None):
            self.submit_tx({"type": "update-client", "for": tx["target"]})
        tx_type = tx.get("type", None)

        # Handle LS Propagations
        # This is to avoid loops
        if tx_type == "link-state-propagation" and self.id not in tx.get(
            "call-stack", []
        ):
            store_tx = {**tx}
            store_tx.pop("target")
            store_tx["from"] = from_
            store_tx["store"] = True
            self.submit_tx(store_tx)

            for c in self.connections:
                self.submit_tx(
                    {
                        "type": "link-state-propagation",
                        "connection_changes": tx.get("connection_changes", {}),
                        "target": c,
                        "call-stack": [*tx["call-stack"], self.id],
                    }
                )

        if tx_type == "cross_chain":
            store_tx = {**tx}
            store_tx.pop("target")
            store_tx["store"] = True
            store_tx["from"] = from_
            self.submit_tx(store_tx)

        self.submit_tx({"type": "ack", "hash": tx["hash"], "target": from_})

    # relayer
    def relay_ack(self, tx: dict, update_client=True):
        if update_client and tx.get("target", None):
            self.submit_tx({"type": "update-client", "for": tx["target"]})
        self.submit_tx({"type": "recv-ack", "hash": tx["hash"]})

    # relayer
    def relay_timeout(self, tx: str, update_client=True):
        if update_client and tx.get("target", None):
            self.submit_tx({"type": "update-client", "for": tx["target"]})
        self.submit_tx({"type": "recv-timeout", "hash": tx["hash"]})

    # core
    def start(self):
        while True:
            block_time = self.config.get("block_time", 10)
            yield self.env.timeout(block_time)
            if self.mempool:
                it = []
                self.block_seq += 1
                for tx in self.mempool:
                    tx["block"] = self.block_seq
                    tx["time"] = float(self.env.now)
                    if tx["type"] == "create-client":
                        # self.connections.append(tx["target"])
                        self.network.add_edge(self.id, tx["target"])
                    if tx["type"] == "link-state-propagation":
                        self.network = compose(self.network, tx.get("network_state", Graph()))
                        changes = tx.get("connection_changes", {})
                        for c, v in changes.items():
                            c1, c2 = c.split("-")
                            self.network.add_edge(c1, c2)
                    it.append(tx)
                self.tx_list.extend(it)
                self.mempool = []
