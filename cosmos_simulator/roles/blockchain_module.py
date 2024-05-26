from abc import ABC, abstractmethod


class BlockchainModule(ABC):
    @abstractmethod
    def call(self, *args, **kwargs): ...

    @abstractmethod
    def handle(self, tx): ...
