import pytest

from tests.utils import expect_no_raises


class BaseObject:
    """
    Inherit pure python object class

    """

    def __init__(self):
        self.attr = "I am Base"


class HashOnlyObject:
    """
    Override __hash__ only class
    """

    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return f"C({self.x})"

    def __hash__(self):
        return hash(self.x)


class EqOnlyObject:
    """
    Override __eq__ only class
    """

    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return f"C({self.x})"

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and
                self.x == other.x
        )


class CompleteEqualityObject:
    """
    Override __eq__ and __hash__ class
    """

    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return f"C({self.x})"

    def __hash__(self):
        return hash(self.x)

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and
                self.x == other.x
        )


@pytest.mark.current
class EqualityTests:
    """
    By default, those methods are inherited from the object class that compares two instances by their identity
    therefore instances are only equal to themselves.
    """

    def test_base_object_equality_is_based_on_identity(self):
        a = BaseObject()
        b = BaseObject()

        assert a != b
        assert a is not b

    def test_base_object_equality_does_not_matter_instance_attribute(self):
        a = BaseObject()
        b = a

        b.attr = "I am Changed"

        assert id(a) is not id(b)
        assert id(a) == id(b)
        assert a == b
        assert a is b

    @expect_no_raises
    def test_base_object_does_contains_hash(self):
        a = BaseObject()

        hash(a)

    def test_hash_changed_if_attribute_is_changed(self):
        one = HashOnlyObject(1)

        old_hash = hash(one)

        one.x = 2
        new_hash = hash(one)

        assert old_hash != new_hash
        assert old_hash is not new_hash

    def test_hash_is_same_when_value_is_same(self):
        one = HashOnlyObject(1)
        another = HashOnlyObject(1)

        assert hash(one) == hash(another)
        assert hash(one) is hash(another)

    def test_hash_is_not_same_when_value_is_not_same(self):
        one = HashOnlyObject(1)
        two = HashOnlyObject(2)

        assert hash(one) != hash(two)
        assert hash(one) is not hash(two)

    def test_hash_does_not_ensure_equlity(self):
        one = HashOnlyObject(1)
        other = HashOnlyObject(1)

        assert one != other
        assert one is not other

    def test_eq_ensure_equlity(self):
        one = EqOnlyObject(1)
        other = EqOnlyObject(1)

        assert one == other

    def test_when_override_only_eq_generate_unhashable_type_error(self):
        one = EqOnlyObject(1)
        with pytest.raises(TypeError) as err:
            hash(one)

        assert err.value.args[0] == f"unhashable type: '{one.__class__.__name__}'"

    def test_hashable_object_eq_ensures_hash_is_also_same(self):
        """
        Two objects that compare equal must also have the same hash value.
        """
        one = CompleteEqualityObject(1)
        other_one = CompleteEqualityObject(1)

        assert one == other_one
        assert hash(one) == hash(other_one)
