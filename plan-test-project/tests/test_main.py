from plan_test_project.main import add


def test_add() -> None:
    assert add(2, 2) == 4
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
