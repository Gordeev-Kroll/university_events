from abc import ABC, abstractmethod
from typing import List

class AggregateStrategy(ABC):
    @abstractmethod
    def calculate(self, values: List[int]) -> float:
        pass

class SumStrategy(AggregateStrategy):
    def calculate(self, values: List[int]) -> float:
        return sum(values)

class AvgStrategy(AggregateStrategy):
    def calculate(self, values: List[int]) -> float:
        return sum(values) / len(values) if values else 0

class MaxStrategy(AggregateStrategy):
    def calculate(self, values: List[int]) -> float:
        return max(values) if values else 0