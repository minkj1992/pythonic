import pytest
from pydantic import ValidationError

from pydantic_django.models import Song


def test_song():
    song = Song(id=1, name="I can almost see you")
    assert False
    assert song.name == "I can almost see you"

    with pytest.raises(expected_exception=ValidationError):
        Song(id=1)
    with pytest.raises(expected_exception=ValidationError):
        Song(id='1')
    with pytest.raises(expected_exception=ValidationError):
        Song(id='foo', name='I can almost see you')
