from cosmos_simulator.core.config import BlockchainConfig
from cosmos_simulator.core.contract import Contract
from cosmos_simulator.core.transaction import Transaction, TransactionState
from simpy import Environment


class Block:
    txs: list[Transaction]
    seq_no: int
    time: float


class Blockchain:
    contracts: dict[str, Contract]
    balances: dict[str, int]
    mempool: list[Transaction]
    env: Environment
    config: BlockchainConfig
    blocks: list[Block]
    id: str

    def __init__(self, id: str, env: Environment, config: BlockchainConfig):
        self.id = id
        self.contracts = {}
        self.balances = {}
        self.mempool = []
        self.env = env
        self.config = config

    def deploy(self, addr: str, contract: Contract, precompile=True):
        if precompile:
            self.contracts[addr] = contract
        else:
            raise NotImplementedError()

    def send(self, tx: Transaction):
        self.mempool.append(tx)

    def start(self):
        while True:
            # Block Generation Time
            block_time = self.config.block_time
            yield self.env.timeout(block_time)

            if self.mempool:
                block = Block()
                block.txs = []
                block.time = float(self.env.now)

                # Find Last SeqNo
                if len(self.blocks) == 0:
                    seq = 0
                else:
                    seq = self.blocks[-1].seq_no + 1
                block.seq_no = seq

                for tx in self.mempool:
                    tx.block = block.seq_no
                    tx.time = float(self.env.now)

                    tg = tx.target
                    try:
                        contract = self.contracts[tg]
                        contract.call(tx)
                        tx.state = TransactionState.ACCEPTED
                        block.txs.append(tx)
                    except Exception as e:
                        tx.state = TransactionState.REJECTED
                        print("Fucked up TX", e)

                self.blocks.append(block)
                self.mempool = []
