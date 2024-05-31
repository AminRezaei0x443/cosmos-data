class BlockchainConfig:
    block_time: int = 10

    def __init__(self, **kwargs):
        self.block_time = kwargs.pop("block_time", 10)
