from abc import ABC, abstractmethod


class Colors(ABC):
    @abstractmethod
    def __init__(self):
        pass

    ZINC_500 = "#71717a"
    GRAY_800 = "#1f2937"
