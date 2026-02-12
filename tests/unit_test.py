from src.common_library import add, subtract

def test_add():
    test_var = "test"
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(5, 3) == 2