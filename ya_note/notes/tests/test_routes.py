from http import HTTPStatus

from notes.tests.core import URL, CoreTestCase, AUTHOR, USER, ANON


class TestRoutes(CoreTestCase):
    def test_pages_availability_for_anonymous_user(self):
        """Проверка доступности страниц анонимному пользователю."""
        URLS = (
            (URL.home, self.client, HTTPStatus.OK, ANON),
            (URL.login, self.client, HTTPStatus.OK, ANON),
            (URL.logout, self.client, HTTPStatus.OK, ANON),
            (URL.signup, self.client, HTTPStatus.OK, ANON),
            (URL.edit, self.author_client, HTTPStatus.OK, AUTHOR),
            (URL.edit, self.user_client, HTTPStatus.NOT_FOUND, USER),
            (URL.delete, self.author_client, HTTPStatus.OK, AUTHOR),
            (URL.delete, self.user_client, HTTPStatus.NOT_FOUND, USER),
            (URL.add, self.user_client, HTTPStatus.OK, USER),
            (URL.list, self.user_client, HTTPStatus.OK, USER),
            (URL.success, self.user_client, HTTPStatus.OK, USER),
            (URL.detail, self.author_client, HTTPStatus.OK, AUTHOR),
            (URL.detail, self.user_client, HTTPStatus.NOT_FOUND, USER),
        )
        for url, client, expected_status, user in URLS:
            with self.subTest(url=url):
                self.assertEqual(
                    client.get(url).status_code,
                    expected_status,
                    msg=(
                        f'Код ответа страницы {url} для {user} не '
                        f'соответствует ожидаемому.'
                    ),
                )

    def test_redirects(self):
        """Проверка редиректа для неавторизованного пользователя."""
        URLS = (
            URL.list,
            URL.add,
            URL.success,
            URL.detail,
            URL.edit,
            URL.delete,
        )
        for url in URLS:
            with self.subTest(url=url):
                redirect_url = f'{URL.login}?next={url}'
                self.assertRedirects(
                    self.client.get(url),
                    redirect_url,
                    msg_prefix=(
                        f'Убедитесь, что у неавторизованного '
                        f'пользователя нет доступа к странице {url}.'
                    ),
                )
