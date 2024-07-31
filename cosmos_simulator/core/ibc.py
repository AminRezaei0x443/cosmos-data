import typing

from cosmos_simulator.core.contract import Contract
from cosmos_simulator.core.transaction import Transaction, TransactionState
from cosmos_simulator.types.ibc_packet import Packet

if typing.TYPE_CHECKING:
    from cosmos_simulator.core.blockchain import Blockchain


class IBC(Contract):
    connections: list[str]
    channels: dict[str, list[str]]
    mh_tunnels: dict[str, (int, int)]
    packets: dict[int, Packet]

    def __init__(self, chain: "Blockchain"):
        super().__init__(chain)
        self.connections = []
        self.channels = {}
        self.packets = {}

    def connect(self, chain: str = None, **kwargs) -> None:
        if chain is None:
            raise ValueError("Chain cannot be None")
        if chain not in self.channels:
            self.channels[chain] = []
        self.connections.append(chain)
        self.channels[chain].append("default")

    def disconnect(self, chain: str = None, **kwargs) -> None:
        if chain is None:
            raise ValueError("Chain cannot be None")
        if chain not in self.connections:
            raise ValueError("Chain is not connected")
        self.connections.remove(chain)
        self.channels.pop(chain)

    def state_dict(self):
        return {
            "connections": self.connections,
            "packets": {k: v.to_dict() for k, v in self.packets.items()},
            "channels": self.channels,
        }

    def load_state_dict(self, state: dict):
        self.connections = state.get("connections", [])

        pkV = state.get("packets", {})
        self.packets = {k: Packet.from_dict(v) for k, v in pkV.items()}

        self.channels = state.get("channels", {})

    def create_channel(self, chain: str, name: str, **kwargs) -> None:
        if chain not in self.channels:
            self.channels[chain] = []
        self.channels[chain].append(name)

    def create_multi_hop_channel(self, chains: list[str], **kwargs) -> None:
        pass

    def send_packet(self, target_chain: str) -> None:
        pass

    def recv_packet(self, src_chain: str) -> None:
        pass
    
    def recv_ack(self, packet_id: int) -> None:
        pass
    
    def recv_timeout(self, packet_id: int) -> None:
        pass
    
    def call(self, tx: Transaction):
        dx = {**tx.data}
        method = dx.pop("method", None)
        if method is None:
            raise ValueError("Method cannot be None")
        if method == "connect":
            self.connect(**dx)
        elif method == "disconnect":
            self.disconnect(**dx)
        elif method == "create-channel":
            self.create_channel(**dx)
        elif method == "send-packet": 
            self.send_packet(**dx)
        elif method == "recv-packet": 
            self.recv_packet(**dx)
        elif method == "recv-ack": 
            self.recv_ack(**dx)
        elif method == "recv-timeout": 
            self.recv_timeout(**dx)
        else:
            raise ValueError("Method is not supported")

    def get_method(self, method: str, **params):
        if method == "get_connections":
            return self.connections
        raise ValueError("Method is not supported")
