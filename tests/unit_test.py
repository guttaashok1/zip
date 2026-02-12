from src.common_library import add, subtract

def test_add():
    assert add(3, 3) == 6

def test_subtract():
    assert subtract(5, 3) == 2