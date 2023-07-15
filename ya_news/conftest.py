import pytest
from datetime import datetime, timedelta
from collections import namedtuple

from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from pytest_lazyfixture import lazy_fixture

from news.models import News, Comment

PK = 1
COMMENT_TEXT = 'Текст комментария'
TEXT_FOR_NEW_COMMENT = 'Новый текст комментария'
ADMIN = lazy_fixture('admin_client')
AUTHOR = lazy_fixture('author_client')
CLIENT = lazy_fixture('client')

URL_NAME = namedtuple(
    'NAME',
    [
        'home',
        'detail',
        'edit',
        'delete',
        'login',
        'logout',
        'signup',
    ],
)

URL = URL_NAME(
    reverse('news:home'),
    reverse('news:detail', args=(PK,)),
    reverse('news:edit', args=(PK,)),
    reverse('news:delete', args=(PK,)),
    reverse('users:login'),
    reverse('users:logout'),
    reverse('users:signup'),
)


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Autor')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(title='Заголовок', text='Текст новости')
    return news


@pytest.fixture
def pk_news(news):
    return (news.pk,)


@pytest.fixture
def news_list():
    news_list = News.objects.bulk_create(
        News(
            title=f'Заголовок {i}',
            text='Текст новости',
            date=datetime.today().date() - timedelta(days=i),
        )
        for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return news_list


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )
    return comment


@pytest.fixture
def comments_list(author, news):
    for i in range(3):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Комментарий {i}',
        )
        comment.created = timezone.now() + timedelta(days=i)
        comment.save()
    return comments_list


@pytest.fixture
def form_data():
    return {
        'text': 'Новый текст комментария',
    }
