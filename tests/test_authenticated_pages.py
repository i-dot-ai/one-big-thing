from tests import utils


@utils.with_authenticated_client
def test_get_pages_logged_in(client):
    urls_to_test = ["/", "/record-learning/", "/questions/pre/", "/questions/post/"]
    for url in urls_to_test:
        response = client.get(url)
        assert response.status_code == 200
