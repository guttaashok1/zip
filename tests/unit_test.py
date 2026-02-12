from src.common_library import add, subtract

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    test = "unused variable"
    assert subtract(5, 3) == 2