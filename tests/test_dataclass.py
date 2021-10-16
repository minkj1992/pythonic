from dataclasses import dataclass, FrozenInstanceError

import pytest

from tests.utils import expect_no_raises


@dataclass(frozen=True)
class FrozenPersonDataclass:
    name: str
    age: int


@dataclass
class NoneFrozenPersonDataclass:
    name: str
    age: int


def test_non_frozen_dataclass_not_hashable():
    """dataclass hash"""
    minwook = NoneFrozenPersonDataclass(name="minwook", age=1)

    with pytest.raises(TypeError):
        _ = {minwook: 1}


def test_non_frozen_dataclass_mutable():
    """dataclass mutable"""
    minwook = NoneFrozenPersonDataclass(name="minwook", age=1)

    other = minwook
    assert minwook == other
    assert minwook is other

    other.name = "other"
    assert minwook == other
    assert minwook is other
    assert minwook.name == "other"


@expect_no_raises
def test_frozen_dataclass_hashable():
    minwook = FrozenPersonDataclass(name="minwook", age=1)

    _ = {minwook: 1}



def test_frozen_dataclass_imutable():
    """dataclass mutable"""
    minwook = FrozenPersonDataclass(name="minwook", age=1)

    same_person: FrozenPersonDataclass = minwook
    assert minwook == same_person
    assert minwook is same_person

    with pytest.raises(FrozenInstanceError):
        same_person.name = "other"
