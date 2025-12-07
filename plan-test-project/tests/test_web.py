from plan_test_project.web import app


def test_root_route() -> None:
    """Test that the root route returns HTML containing 'hey'."""
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"hey" in response.data
