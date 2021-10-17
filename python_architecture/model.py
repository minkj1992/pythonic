from __future__ import annotations  # enable forward referencing

from dataclasses import dataclass
from datetime import date
from typing import Optional, Set, List


def allocate(line: OrderLine, batches: List[Batch]):
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStockException(f'Out of stock for sku {line.sku}')


class OutOfStockException(Exception):
    """Out of stock"""


@dataclass(frozen=True)
class OrderLineBase:
    sku: str
    qty: int


@dataclass(frozen=True)
class OrderLine(OrderLineBase):
    id: str


class Batch:
    def __init__(self, ref: str, order_line_base: OrderLineBase, eta: Optional[date]):
        self.reference = ref
        self.sku = order_line_base.sku
        self.eta = eta

        self._purchased_qty = order_line_base.qty
        self._allocations = set()  # type: Set[OrderLine]

    def __repr__(self):
        return f"<Batch {self.reference}>"

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    @property
    def allocated_qty(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_qty(self) -> int:
        return self._purchased_qty - self.allocated_qty

    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine) -> None:
        if line in self._allocations:
            self._allocations.remove(line)

    def can_allocate(self, line) -> bool:
        return (
                self.sku == line._SKU and
                self.available_qty >= line.qty
        )
