from notes.forms import NoteForm
from notes.tests.core import URL, CoreTestCase


class TestNoteList(CoreTestCase):
    def test_notes_list_for_different_users(self):
        """Проверка списка заметок."""
        clients = (
            (self.author_client, True),
            (self.user_client, False),
        )
        for client, value in clients:
            with self.subTest(client=client):
                notes_list = client.get(URL.list).context['object_list']
                self.assertTrue(
                    (self.note in notes_list) is value,
                    msg=(
                        f'{client} не должен видеть заметки других '
                        f'пользователей в своем списке заметок.'
                    ),
                )

    def test_pages_contains_form(self):
        """Проверка: на страницах отображаются формы."""
        for url in (URL.add, URL.edit):
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context['form'],
                    NoteForm,
                    msg=(
                        f'Проверьте, что форма редактирования передается на '
                        f'страницу {url}.'
                    ),
                )
