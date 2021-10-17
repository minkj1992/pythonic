import pytest

from python_architecture.tests.conftest import make_batch_and_line, make_batch, make_order_line

pytestmark = pytest.mark.current
_SKU = 'SMALL-TABLE'


def test_allocating_to_a_batch_reduces_the_available_qty():
    batch, line = make_batch_and_line(_SKU, batch_qty=20, line_qty=2)

    batch.allocate(line)

    assert batch.available_qty == (20 - 2)


def test_can_allocate_if_available_gt_required():
    large_batch, small_line = make_batch_and_line(_SKU, batch_qty=1000, line_qty=2)
    assert large_batch.can_allocate(small_line)


def test_can_allocate_if_availlable_eq_required():
    batch, line = make_batch_and_line(_SKU, batch_qty=2, line_qty=2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_available_lt_required():
    small_batch, large_line = make_batch_and_line(_SKU, batch_qty=2, line_qty=200)
    assert small_batch.can_allocate(large_line) is False


def test_cannot_allocate_if_sku_does_not_matched():
    not_matched_sku = "LARGE-TABLE"
    batch = make_batch(_SKU, 20)
    diff_sku_line = make_order_line(not_matched_sku, 20)
    assert batch.can_allocate(diff_sku_line) is False


def test_allocation_is_idempotent():
    batch, line = make_batch_and_line(_SKU, batch_qty=20, line_qty=2)

    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_qty == 18


def test_deallocate():
    batch, line = make_batch_and_line(_SKU, batch_qty=20, line_qty=2)
    batch.allocate(line)
    batch.deallocate(line)
    assert batch.available_qty == 20


def test_can_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line(_SKU, batch_qty=20, line_qty=2)
    batch.deallocate(unallocated_line)
    assert batch.available_qty == 20
