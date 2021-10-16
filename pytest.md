# `pytest`
> [pytest](est-dev/pytest)는 python을 사용해 `simple`, `readable`한 tests를 짤 수 있는 프레임워크입니다.

다음은 오픈소스에 공유된 pytest를 사용하고 있는 프로젝트들 중 일부 입니다. 대부분의 파이썬을 활용하는 유명 기업들이 사용하고 있는걸 확인할 수 있습니다. (특이하게 구글만 모두 unittest만 사용하는 것을 확인)
- [Microsoft: recommenders](https://github.com/microsoft/recommenders)
- [Microsoft: nni](https://github.com/microsoft/nni/tree/master/test)
- [Microsoft: torchgeo](https://github.com/microsoft/torchgeo/tree/main/tests)
- [Microsoft](https://github.com/microsoft/lightgbm-benchmark/tree/main/tests)
- [Aws: gluon-ts](https://github.com/awslabs/gluon-ts/blob/master/pytest.ini)
- [Uber: ludwig](https://github.com/ludwig-ai/ludwig/blob/master/pytest.ini)
- [NSA: walkoff](https://github.com/nsacyber/WALKOFF)
- [fastapi](https://github.com/tiangolo/fastapi/tree/master/tests)

다음은 실제 django와 pytest를 활용한 오픈소스 서비스입니다.
- [shuup](https://github.com/shuup/shuup)
- [saleor](https://github.com/saleor/saleor)

그렇다면 왜 다수의 기업에서 파이썬 공식 테스트 프레임워크인 [unittest](https://docs.python.org/3/library/unittest.html)를 대신 `pytest`를 사용하는 걸까요?

> 개인적으로 
> 1) parallel 
> 2) fixture 
> 3) Parameterize 기능 때문이라 생각


## 1. Why: pytest vs unittest
> unittest와 비교하여 pytest를 설명합니다. 이외에도 파이썬 생태계에는 `robotframework`, `nose`, `doctest` 프레임워크들이 존재하지만 해당 문서에서는 다루지 않습니다.

자세한 내용은 pytest의 feature에서 보도록 하고, 여기에서는 unittest의 단점 위주로 알아보도록 합시다. 우선 들어가기 앞서 pytest에서 제공하고 있는 주요 기능(장점)들은 다음과 같습니다.

1. `Fixture` 테스트에 필요한 변수들을 주입 가능 (top-down )
2. `Unittest Compatibility` 기존 unittest와 호환된다.
3. `Auto-Discovery of Tests` 테스트를 자동으로 찾아준다.
4. `Parameterization` 하나의 테스트에 여러 파라미터를 넣어줌으로써, 여러번 테스트를 돌릴 수 있다.
5. `Mark`: 원하는 테스트들만 Grouping하여 지정 실행 가능합니다.
6. `assert` assertEqual(), assertGreater()같은 assert 메서드를 적재적소에 사용해야 unittest와 달리 `assert`문 하나로 사용 가능합니다. (자동 분석)
7. `plugins` pytest는 활발히 개발되는 오픈소스로, pytest를 기반으로 개발되는 다양한 플러그인들이 다수 존재합니다. 특히 자주 사용되는 플러그인들은 다음과 같습니다.
    - `xdist`: parallel test 가능
    - `pytest-django`: 간편한 django용 fixture 제공
    - [pytest-cov](https://github.com/pytest-dev/pytest-cov): 테스트 커버리지 분석 및 취약점 웹페이지 제공
    - `pytest-bdd`: Cucumber like bdd를 제공해줌 으로써, unittest에 사용한 pytest fixture들을 재활용 하여 Integration 테스트를 손쉽게 작성 가능


## 2. What: pytest 주요 feature 위주로 설명

### `Fixture`
> Unit test의 `AAA패턴(Arrange/Act/Assert)`중, Fixture`는 `Arrange`, [Act](https://docs.pytest.org/en/6.2.x/fixture.html#fixtures-can-be-requested-more-than-once-per-test-return-values-are-cached) 의 기능을 담당합니다.


unittest는 xUnit 스타일처럼 테스트 초기 환경을 구현하기 위해서는 setUpClass, tearDownClass, setUp, tearDown를 매 케이스마다 구현해주어야 합니다. (중복 발생) 반대로 pytest의 `fixture`는 이를 극적으로 개선하여 중복을 없애고, `확장성`을 높였습니다.

   - 픽스처는 명시적인 이름을 가지며 테스트 함수에서의 선언을 통해 이를 활성화시킬 수 있습니다.
   - 픽스처는 모듈화된 방식으로 구현되어 있습니다. 각 픽스처 이름은 트리거 함수를 호출하고, 또 **그 픽스처 역시 다른 픽스처를 사용할 수 있습니다**.
   - 픽스처 관리를 통해 단순한 유닛 테스트부터 복잡한 기능 테스트에 이르기까지 테스트 규모를 확장할 수 있습니다. 환경 설정이나 컴포넌트 설정에 따라 매개변수화된 픽스처를 정의하는 것도 가능합니다. **픽스처를 함수, 모듈, 또는 전체 테스트 세션 영역에 걸쳐 재사용할 수 있도**록 돕기도 합니다.
   - **fixture의 scope는 디렉토리 위치 기준에서 영향을 줍니다.** [공식문서](https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files)

- unittest
```python
from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.tests import test_utils, test_fixtures

class QrCodeTests(APITestCase):
    multi_db = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ...

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self) -> None:
        pass
    
    def tearDown(self) -> None:
        pass
    
    ... 중략 ...
```

- pytest
  - fixture 외에도 pytest의 hook을 통해서도 stage별 소스 흐름을 제어할 수 있습니다.
```python
# conftest.py
@pytest.fixture(scope="session") # session, module, class, function
def chrome_browser():
    # setUp
    browser =  webdriver.Chrome(chrome_driver)
    yield browser

    # tearDown
    browser.quit()

# test_context.py
def test_login_page(chrome_browser):
    """chrome_browser가 주입"""
```

#### [Teardown/Cleanup (AKA Fixture finalization)](https://docs.pytest.org/en/6.2.x/fixture.html#teardown-cleanup-aka-fixture-finalization)

pytest에서 recommended된 방식은 yield fixtures 방식으로 다음과 같이 사용할 수 있습니다.

```python
# conftest.py
@pytest.fixture
def driver():
    _driver = Chrome()
    yield _driver
    _driver.quit()
```
실제 서비스에서 사용하게 되면 다음과 같이 활용 가능합니다.

```python
@pytest.fixture
def current_member(db, member_factory) -> Member:
    member = member_factory.create()
    yield member
    member.delete()


@pytest.fixture
def current_master(db, current_partner, current_member, member_factory, partner_member_factory):
    master = member_factory.create()

    # create master
    partner_with_master = partner_member_factory.create(partner_id=current_partner.id,
                                                        member_id=master.id,
                                                        is_master=True)

    # invite member
    partner_with_member = partner_member_factory.create(partner_id=current_partner.id,
                                                        member_id=current_member.id,
                                                        inviter_member_id=master.id,
                                                        is_master=False)
    yield master
    master.delete()
    partner_with_master.delete()
    partner_with_member.delete()


@pytest.fixture
def authenticated_client(client, current_member):
    cookies = SimpleCookie({'_kawlt': KAWLT})
    with patch(
            target='apps.auth.services.authentication_kakao_for_biz.KakaoForBizLoginAuthentication.authenticate_credentials',
            return_value=[current_member, None]):
        client.cookies = cookies

        yield client


... 

# qrcodes/test_qrcode.py
@pytest.mark.api
def test_get_qrcode_list(authenticated_client, card, qrcode, current_partner):
    url = reverse('qrcodes:qrcode-list', kwargs={'pid': current_partner.id})
    response = authenticated_client.get(url, format='json')
    assert response.status_code == 200
```

예를 들어 `qrcodes`의 경우

1. 멤버 가입
2. 마스터가 파트너 생성
3. 멤버 또는 마스터가 qrcode 생성

다음과 같은 여러 절차의 setup이 / 중복으로 활용되어야 하지만, conftest를 활용하면 한 곳에서 setup과정을 관리 할 수 있으며 패키지를 나눔으로 써 isolation을 보장할 수 있습니다.



#### [conftest.py](https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files)
> sharing fixtures across multiple files

- `conftest.py`는 실제 `fixtures`들을 정의하는 공간입니다.
- `conftest.py`에 정의된 fixture들은 scope에 따라서 test 파일들에 공유됩니다.
- pytest will automatically discover them. 그러므로 따로 import가 필요하지 않습니다.

특히 **`multiple nested directories/packages`한 환경으로 테스트 환경을 구성할 경우 여러 `conftest.py`를 구성 할 수 있습니다.** 이렇게 하게 될 경우 테스트 실행에 필요한 fixture들을 효율적으로 load시킬 수 있으며, 테스트의 isolation을 증가 시키면서도 fixture들의 재사용성을 극대화 시킬 수 있는 것으로 보입니다.

또한 이렇게 특정 폴더안에 conftest.py를 생성하게 될 경우, 해당 파일에 들어있는 fixture들은 최대 폴더 안에서만 영향을 줄 수 있습니다. (isolation)

**대체로 테스트 디렉토리 구조는 다음 2가지 정도로 구성**
1. doamin 기준
2. test 종류 기준

```
# domain 기준
└── tests
    ├── conftest.py # django client / user login / mock db ..  
    ├── factories.py # model factory들 생성
    └── qrcodes
        ├── __init__.py
        ├── conftest.py # qrcode에 필요한 fixture들 정의
        ├── unit/
        ├── integration/
        └── utils.py
    └── members
        ├── __init__.py
        ├── conftest.py # member에 필요한 fixture들 정의 
        ├── unit/
        ├── integration/
        └── utils.py
    └── partners
        ├── __init__.py
        ├── conftest.py # partners에 필요한 fixture들 정의 
        ├── unit/
        ├── integration/
        └── utils.py
```

```
# test 종류별 정렬 https://github.com/microsoft/recommenders
├── tests
│   ├── conftest.py
│   ├── integration
│   │   ├── __init__.py
│   │   ├── examples
│   │   │   ├── __init__.py
│   │   │   ├── test_notebooks_gpu.py
│   │   │   ├── test_notebooks_pyspark.py
│   │   │   └── test_notebooks_python.py
│   │   └── recommenders
│   │       ├── __init__.py
│   │       └── datasets
│   │           ├── __init__.py
│   │           ├── test_criteo.py
│   │           ├── test_mind.py
│   │           └── test_movielens.py
│   ├── smoke
│   │   ├── __init__.py
│   │   └── recommenders
│   │       ├── __init__.py
│   │       ├── dataset
│   │       │   ├── __init__.py
│   │       │   ├── test_criteo.py
│   │       │   ├── test_mind.py
│   │       │   └── test_movielens.py
│   │       └── recommender
│   │           ├── __init__.py
│   │           ├── test_deeprec_model.py
│   │           ├── test_deeprec_utils.py
│   │           ├── test_newsrec_model.py
│   │           └── test_newsrec_utils.py
│   └── unit
│       └── recommenders
│           ├── __init__.py
│           ├── datasets
│           │   ├── __init__.py
│           │   ├── test_covid_utils.py
│           │   ├── test_dataset.py
│           │   └── test_wikidata.py
│           ├── models
│           │   ├── __init__.py
│           │   └── test_wide_deep_utils.py
│           ├── tuning
│           │   ├── __init__.py
│           │   ├── test_nni_utils.py
│           │   └── test_sweep.py
│           └── utils
│               ├── __init__.py
│               ├── test_general_utils.py
│               └── test_timer.py
```

### Parameterization
> = for loop

```python
from pytest import mark


@mark.parametrize('company', [
        ("naver"),
        ("kakao"),
        ("microsoft"),
        ("github")
    ]
)
def test_company_with_decorator_param(company):
    assert validate_company(company) == True
```

### Mark
> marking을 해서 원하는 테스트만 진행 가능

- [microsoft recommender](https://github.com/microsoft/recommenders/blob/27709229cdc4aa7d39ab715789f093a2d21d2661/tox.ini#L57)를 예로 들면

```
[pytest]
markers = 
    # markers allow to us to run faster subset of the test:
    # EX: pytest -m "not spark and not gpu"
    # See https://docs.pytest.org/en/stable/example/markers.html#registering-markers
    deeprec: test deeprec model
    sequential: test sequential model
    notebooks: mark a test as notebooks test
    smoke: mark a test as smoke test
    integration: mark a test as integration test
    gpu: mark a test as gpu test
    spark: mark a test as spark test
    vw: mark a test as vowpal wabbit test
```

```python
from recommenders.datasets import criteo


@pytest.mark.integration
def test_criteo_load_pandas_df(criteo_first_row):
    ...중략...
```




### plugins
> xdist, cov

- pytest-cov
```bash
$ pytest --cov

---------- coverage: platform darwin, python 3.8.6-final-0 -----------
Name                            Stmts   Miss  Cover
---------------------------------------------------
pydantic_django/models.py           4      0   100%
pydantic_tutorial/__init__.py       1      0   100%
pydantic_tutorial/example.py       60     10    83%
tests/__init__.py                   0      0   100%
tests/conftest.py                  16      0   100%
tests/test_pydantic.py             11      0   100%
tests/test_pydantic_django.py      13      7    46%
tests/utils.py                      9      2    78%
---------------------------------------------------
TOTAL                             114     19    83%
```
- pytest-html
```bash
$ pip install pytest-html
$ pytest --html="report.html"  # html
$ pytest --junitxml="report.xml" # for jenkins ci
```

![](https://github.com/minkj1992/Python/raw/master/pytest/assets/1.png)
![](https://github.com/minkj1992/Python/raw/master/pytest/assets/2.png)
![](https://github.com/minkj1992/Python/raw/master/pytest/assets/3.png)

- pytest-xdist
```bash
$ pytest --numprocesses auto # cpu 수에 맞춰 프로세스 진행
```

## 3. pytest command
```bash
$ pytest # pytest.ini 세팅 기반으로 pytest 실행
$ pytest --collect-only # pytest가 검사할 파일들만 찾음
$ pytest -v # 더 자세히 show
$ pytest -s # captures standard output
$ pytest -m api
$ pytest -m "not api"
$ pytest -m "api and db"
```

## 4. pytest setup
### pytest.ini
> 
```
[pytest]
python_files = test_*
python_classes = *Tests
python_functions = test_*

# addopts = -m api -v -s -cov --reuse-db --create-db tb=short --numprocesses auto
# --create-db: 스키마 변경 시 사용
# --reuse-db: 기존 db 스키마 그대로 사용
addopts =
    -m api
    -s
    -p no:warnings
    --numprocesses=auto
testpaths =
    tests

# settings 위치
DJANGO_SETTINGS_MODULE = icp.settings.test

markers =
    api: All api tests
    model: All api tests
    service: All api tests
    unit: All unit tests
```

## 5. pytest load data
1. factory boy + faker을 사용하는 방법
    - 매번 테스트 할 때마다, fake 데이터 기반의 model을 생성 가능
    - [factories](./factories.py) 
    - [활용 예시](./conftest.py)

2. [read json example](https://github.com/minkj1992/pythonic/tree/main/tests)을 사용하는 방법
   1. 에러 데이터가 어떤 이유로 에러가 나타나고 있는지 설명하기 어렵다. 


## 6. pytest mock

### django client mock

```python
# tests/conftest.py
@pytest.fixture
def authenticated_client(client, current_member):
    cookies = SimpleCookie({'_kawlt': KAWLT})
    with patch(
            target='apps.auth.services.authentication_kakao_for_biz.KakaoForBizLoginAuthentication.authenticate_credentials',
            return_value=[current_member, None]):
        client.cookies = cookies

        yield client

# tests/qrcodes/test_qrcode.py
def test_get_qrcode_list(authenticated_client):
    url = reverse('qrcodes:qrcode-list')
    response = authenticated_client.get(url, format='json')
    assert response.status_code == 200
```
 
### sql db mock
> in-memory sqlite3를 사용합니다.

```python
# pytest.ini
DJANGO_SETTINGS_MODULE = icp.settings.test

# icp/settings/tests.py
... 중략 ...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'icp',
    },
    'icp_separated': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'icp_separated',
    }
}
```

### mongodb mock
> in-memory mongodb를 사용합니다.
```python
# pytest.ini
DJANGO_SETTINGS_MODULE = icp.settings.test

# icp/settings/tests.py
... 중략 ...
mongoengine.connect('icp', host='mongomock://localhost')
```

