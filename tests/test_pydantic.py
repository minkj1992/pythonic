import pytest
from pydantic import ValidationError

from pydantic_tutorial import Book
from pydantic_tutorial.example import ISBN10FormatError, ISBNMissingError
from tests.utils import expect_no_raises


@expect_no_raises
def test_book(valid_book):
    Book(**valid_book)


def test_invalid_book(invalid_book):
    with pytest.raises(expected_exception=(
            ValidationError,
            ISBNMissingError,
            ISBN10FormatError)):
        Book(**invalid_book)
