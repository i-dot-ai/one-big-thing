from .utils import with_client


@with_client
def test_add_evaluation(client):
    response = client.get("/")
    assert response.status_code == 302


@with_client
def test_urls_no_access(client):
    urls_to_test = ["/record-learning/", "/", "/test/"]
    for url in urls_to_test:
        response = client.get(url)
        assert response.status_code == 302


@with_client
def test_get_login(client):
    response = client.get("/accounts/login/")
    assert response.status_code == 200
