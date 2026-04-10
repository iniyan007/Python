from decorators import test, skip, parametrize
from fixtures import fixture


@fixture()
def sample_data():
    return 10


@test
def test_simple():
    assert 1 + 1 == 2


@test
@parametrize("x,y", [(1,2), (2,3), (5,6)])
def test_add(x, y):
    assert x + 1 == y


@test
def test_with_fixture(sample_data):
    assert sample_data == 10


@test
@skip("Not implemented")
def test_skip_example():
    assert False