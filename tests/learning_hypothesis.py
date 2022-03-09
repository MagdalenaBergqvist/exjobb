import pytest
from hypothesis import given
from hypothesis.strategies import lists, integers


def fail_sort(list):
  return sorted(list)

@given(lists(integers()))
def test_sort(lista):
    assert(fail_sort(lista) == sorted(lista))

@given(lists(integers()))
def test_sortxd(lista):
    assert(fail_sort(lista) == sorted(lista[0]))
