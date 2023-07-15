from datetime import date

import pytest
from django.conf import settings
from django.utils import timezone

from conftest import URL
from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count_order(client, news_list):
    """Проверка: новости выводятся по дате и в нужном кол-ве."""
    response = client.get(URL.home)
    object_list = list(response.context['object_list'])
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE
    assert isinstance(object_list[0].date, date)
    assert object_list == sorted(
        object_list, key=lambda x: x.date, reverse=True
    )


def test_comments_order(client, news, comments_list):
    """Проверка: комментарии сортируется."""
    response = client.get(URL.detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = list(news.comment_set.all())
    assert isinstance(all_comments[0].created, timezone.datetime)
    assert all_comments == sorted(all_comments, key=lambda x: x.created)


def test_client_has_accessed_to_form(client, admin_client, news):
    """Проверка доступности формы комментария и её типа."""
    response = client.get(URL.detail)
    admin_response = admin_client.get(URL.detail)
    assert (
        isinstance(admin_response.context['form'], CommentForm)
        and 'form' not in response.context
    )
