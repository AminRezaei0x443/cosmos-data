from abc import ABC, abstractmethod


class Contract(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def call(self, *args, **kwargs):
        pass
