from enum import Enum


class PacketState(Enum):
    PACKET_STATE_COMMITTED = 0
    PACKET_STATE_ACK = 1
    PACKET_STATE_TIMED_OUT = 2
    PACKET_STATE_FAILED = 3


class Packet:
    destination_chain: str
    connection_id: int
    channel_id: str
    state: PacketState

    def __init__(
        self,
        destination_chain: str,
        connection_id: int,
        channel_id: str,
        state: PacketState,
    ):
        self.destination_chain = destination_chain
        self.connection_id = connection_id
        self.channel_id = channel_id
        self.state = state

    def to_dict(self):
        return {
            "destination_chain": self.destination_chain,
            "connection_id": self.connection_id,
            "channel_id": self.channel_id,
            "state": self.state.value,
        }

    @staticmethod
    def from_dict(data: dict):
        destination_chain = data.get("destination_chain")
        connection_id = data.get("connection_id")
        channel_id = data.get("channel_id")
        state = data.get("state")
        return Packet(destination_chain, connection_id, channel_id, state)
