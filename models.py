from dataclasses import dataclass
from abc import ABC, abstractmethod

import pedigree_matrix as pm
import numpy as np

from vars import *


class Amount(ABC):
    @abstractmethod
    def draw_value(self) -> float:
        pass


@dataclass
class AmountWithNoUncertainty(Amount):
    value: float

    def draw_value(self) -> float:
        return self.value


@dataclass
class AmountWithPedigreeUncertainty(Amount):
    value: float
    reliability: int
    completeness: int
    temporal_correlation: int
    geographical_correlation: int
    technological_correlation: int

    def __post_init__(self):
        for category in (
            self.reliability,
            self.completeness,
            self.temporal_correlation,
            self.geographical_correlation,
            self.technological_correlation,
        ):
            if category not in (1, 2, 3, 4, 5):
                raise ValueError("All pedigree matrix values should be between 1 and 5")

    def draw_value(self) -> float:
        matrix = pm.PedigreeMatrix(version=2)
        matrix.from_numbers(
            self.reliability,
            self.completeness,
            self.temporal_correlation,
            self.geographical_correlation,
            self.technological_correlation,
        )
        sigma = matrix.calculate(basic_uncertainty=BASIC_UNCERTAINTY)
        return np.random.lognormal(np.log(self.value), sigma)


class Product(ABC):
    @abstractmethod
    def draw_impact(self) -> float:
        pass


@dataclass
class BaseProduct(Product):
    name: str
    unit: str
    impact: Amount

    def draw_impact(self) -> float:
        return self.impact.draw_value()


@dataclass
class ProductUsage:
    product: Product
    amount: Amount


@dataclass
class CompoundProduct(Product):
    name: str
    unit: str
    usages: list[ProductUsage]

    def draw_impact(self) -> float:
        return sum(
            usage.amount.draw_value() * usage.product.draw_impact()
            for usage in self.usages
        )
