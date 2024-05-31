from cosmos_simulator.core.config import BlockchainConfig
from cosmos_simulator.core.contract import Contract
from cosmos_simulator.core.transaction import Transaction, TransactionState
from simpy import Environment

from cosmos_simulator.util.log import log


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
        self.blocks = []
        self.env = env
        self.config = config

    def deploy(self, addr: str, contract: Contract, precompile=True):
        if precompile:
            self.contracts[addr] = contract
        else:
            raise NotImplementedError()

    def send(self, tx: Transaction):
        self.mempool.append(tx)

    def run_method(self, target: str, method: str, **params):
        if target not in self.contracts:
            raise KeyError(f"Target Contract {target} is not deployed")
        contract = self.contracts[target]
        return contract.get_method(method, **params)

    def start(self):
        while True:
            # Block Generation Time
            block_time = self.config.block_time
            yield self.env.timeout(block_time)

            log(
                "chain",
                self.id,
                "mempool-start",
                self.env.now,
                f"len: {len(self.mempool)}",
            )
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

                log(
                    "chain", self.id, "block-start", self.env.now, f"id: {block.seq_no}"
                )
                for tx in self.mempool:
                    tx.block = block.seq_no
                    tx.time = float(self.env.now)

                    tg = tx.target
                    try:
                        contract = self.contracts[tg]
                        contract.call(tx)
                        tx.state = TransactionState.ACCEPTED
                        block.txs.append(tx)
                        log(
                            "chain",
                            self.id,
                            "tx-add",
                            self.env.now,
                            f"target: {tx.target}",
                        )
                    except Exception as e:
                        tx.state = TransactionState.REJECTED
                        log(
                            "chain",
                            self.id,
                            "tx-fail",
                            self.env.now,
                            f"error: {e}",
                        )

                self.blocks.append(block)
                self.mempool = []
                log(
                    "chain",
                    self.id,
                    "block-end",
                    self.env.now,
                    f"id: {block.seq_no}, len: {len(block.txs)}",
                )
