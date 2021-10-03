import json
from os.path import abspath, dirname, join
from typing import List, Dict

import pytest


def load_params_from_json(file_name: str) -> List[Dict]:
    root_path = dirname(abspath(__file__))
    file_path = join(root_path, file_name)
    with open(file_path) as f:
        return json.load(f)


@pytest.fixture(scope="session", params=load_params_from_json('books.json'))
def valid_book(request):
    return request.param


@pytest.fixture(scope="session", params=load_params_from_json('invalid_books.json'))
def invalid_book(request):
    """
    json을 통해 데이터를 가져올 경우, 발생할 Exception을 매핑 시키기 어려우며,
    어떤 에러 데이터 인지 명시적으로 보여지지 않는다는 단점이 발생
    """
    return request.param
