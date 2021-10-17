from datetime import date, timedelta

import pytest
from faker import Faker
from python_architecture.model import Batch, OrderLine, OrderLineBase

fake = Faker('ko_KR')


@pytest.fixture(scope='session')
def today():
    return date.today()


@pytest.fixture(scope='session')
def tomorrow(today):
    return today + timedelta(days=1)


@pytest.fixture(scope='session')
def later(tomorrow):
    return tomorrow + timedelta(days=10)


def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        make_batch(sku, batch_qty),
        make_order_line(sku, line_qty)
    )


def make_batch(sku, batch_qty) -> Batch:
    ref = _get_ref(prefix='batch')
    return Batch(ref,
                 OrderLineBase(sku=sku, qty=batch_qty),
                 eta=date.today())


def make_order_line(sku, line_qty) -> OrderLine:
    ref = _get_ref(prefix='order')
    return OrderLine(id=ref, sku=sku, qty=line_qty)


def _get_ref(prefix) -> str:
    num = fake.pyint(min_value=1, max_value=999)
    return f'{prefix}-{str(num).zfill(3)}'
