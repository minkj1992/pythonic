import pytest

from python_architecture.model import allocate, OrderLine, Batch, OutOfStockException, OrderLineBase
from python_architecture.tests.conftest import make_order_line, make_batch

pytestmark = pytest.mark.current

_SKU = 'RETRO-CLOCK'


def test_prefers_current_stock_batches_to_shipments(today):
    in_stock_batch = make_batch(_SKU, 100, eta=None)
    shipment_batch = make_batch(_SKU, 100, eta=today)
    line = make_order_line(_SKU, 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_qty == 90
    assert shipment_batch.available_qty == 100


def test_prefers_earlier_batches(today, tomorrow, later):
    earliest = make_batch(_SKU, 100, eta=today)
    medium = make_batch(_SKU, 100, eta=tomorrow)
    latest = make_batch(_SKU, 100, eta=later)
    line = make_order_line(_SKU, 10)

    allocate(line, [earliest, medium, latest])

    assert earliest.available_qty == 90
    assert medium.available_qty == 100
    assert latest.available_qty == 100


def test_returns_allocated_batch_ref(tomorrow):
    in_stock_batch = make_batch(_SKU, 100, eta=None)
    shipment_batch = make_batch(_SKU, 100, eta=tomorrow)
    line = make_order_line(_SKU, 10)

    allocation = allocate(line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.ref


def test_raises_out_of_stock_exception_if_cannot_allocate(today):
    batch = make_batch(_SKU, 100, eta=today)
    line = make_order_line(_SKU, 100)
    out_of_stock_line = make_order_line(_SKU, 100)

    allocate(line, [batch])

    # match: regular expression matches on the string representation of an exception
    with pytest.raises(OutOfStockException, match=_SKU):
        allocate(out_of_stock_line, [batch])
