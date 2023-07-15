from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from conftest import URL, ADMIN, AUTHOR, CLIENT

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (URL.home, CLIENT, HTTPStatus.OK),
        (URL.signup, CLIENT, HTTPStatus.OK),
        (URL.login, CLIENT, HTTPStatus.OK),
        (URL.logout, CLIENT, HTTPStatus.OK),
        (URL.edit, AUTHOR, HTTPStatus.OK),
        (URL.edit, ADMIN, HTTPStatus.NOT_FOUND),
        (URL.delete, AUTHOR, HTTPStatus.OK),
        (URL.delete, ADMIN, HTTPStatus.NOT_FOUND),
        (URL.detail, CLIENT, HTTPStatus.OK),
    ),
)
def test_anonymous_user_has_access_to_pages(
    url, parametrized_client, expected_status, comment
):
    """Проверка доступности страниц для анонимного пользователя."""
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (URL.edit, URL.delete),
)
def test_anonymus_client_redirect_to_login_page(client, url, comment):
    """Проверка редиректа для анонимного пользователя."""
    expected_url = f'{URL.login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
