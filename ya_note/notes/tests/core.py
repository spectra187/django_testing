from collections import namedtuple

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

USER_MODEL = get_user_model()
SLUG = 'note-slug'
AUTHOR = 'Автор'
USER = 'Пользователь'
ANON = 'anonymous'
FIELD_NAMES = ('title', 'text', 'slug', 'author')
FIELD_DATA = ('Заголовок', 'Текст заметки', SLUG)
FIELD_NEW_DATA = ('Новый заголовок', 'Новый текст', 'new-slug')

URL_NAME = namedtuple(
    'NAME',
    [
        'home',
        'add',
        'list',
        'detail',
        'edit',
        'delete',
        'success',
        'login',
        'logout',
        'signup',
    ],
)

URL = URL_NAME(
    reverse('notes:home'),
    reverse('notes:add'),
    reverse('notes:list'),
    reverse('notes:detail', args=(SLUG,)),
    reverse('notes:edit', args=(SLUG,)),
    reverse('notes:delete', args=(SLUG,)),
    reverse('notes:success'),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
)


class CoreTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = USER_MODEL.objects.create(username=AUTHOR)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.user = USER_MODEL.objects.create(username=USER)
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.note = Note.objects.create(
            **dict(zip(FIELD_NAMES, (*FIELD_DATA, cls.author)))
        )
