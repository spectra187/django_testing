from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from conftest import URL, COMMENT_TEXT, TEXT_FOR_NEW_COMMENT
from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_anonymous_cant_create_comment(client, news, form_data):
    """Проверка: анонимный пользователь не может оставить комментарий."""
    expected_comments_count = Comment.objects.count()
    client.post(URL.detail, data=form_data)
    factual_comments_count = Comment.objects.count()
    assert expected_comments_count == factual_comments_count


def test_logged_can_create_comment(author_client, author, news, form_data):
    """Проверка: авторизованный пользователь может оставить комментарий."""
    expected_comments_count = Comment.objects.count() + 1
    response = author_client.post(URL.detail, data=form_data)
    factual_comments_count = Comment.objects.count()
    comment = Comment.objects.get()
    assertRedirects(response, f'{URL.detail}#comments')
    assert expected_comments_count == factual_comments_count
    assert all(
        (
            comment.text == form_data['text'],
            comment.author == author,
            comment.news == news,
        )
    )


@pytest.mark.parametrize('word', BAD_WORDS)
def test_user_cant_use_bad_words(author_client, news, word):
    """Проверка наличия запрещенных слов в форме."""
    expected_comments_count = Comment.objects.count()
    bad_words_data = {'text': f'плохое слово ->, {word}, <-плохое слово'}
    response = author_client.post(URL.detail, data=bad_words_data)
    factual_comments_count = Comment.objects.count()
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert expected_comments_count == factual_comments_count


def test_author_can_delete_comment(author_client, comment, pk_news):
    """Проверка возможности удаления комментария автором."""
    expected_comments_count = Comment.objects.count() - 1
    response = author_client.delete(URL.delete)
    factual_comments_count = Comment.objects.count()
    assertRedirects(response, f'{URL.detail}#comments')
    assert expected_comments_count == factual_comments_count


def test_user_cant_delete_comment_of_another_user(admin_client, comment):
    """Проверка: никто кроме автора не может удалить комментарий."""
    expected_comments_count = Comment.objects.count()
    response = admin_client.delete(URL.delete)
    factual_comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert expected_comments_count == factual_comments_count


def test_author_can_edit_comment(
    author, author_client, comment, pk_news, form_data
):
    """Проверка: редактировать комментарий может только автор."""
    expected_comments_count = Comment.objects.count()
    response = author_client.post(URL.edit, data=form_data)
    assertRedirects(response, f'{URL.detail}#comments')
    comment.refresh_from_db()
    factual_comments_count = Comment.objects.count()
    assert expected_comments_count == factual_comments_count
    assert all((
        comment.text == TEXT_FOR_NEW_COMMENT,
        comment.author == author
    ))


def test_user_cant_edit_comment_of_another_user(
    author, admin_client, comment, pk_news, form_data
):
    """Проверка: нельзя редактировать чужие комментарии."""
    expected_comments_count = Comment.objects.count()
    response = admin_client.post(URL.edit, data=form_data)
    comment.refresh_from_db()
    factual_comments_count = Comment.objects.count()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert expected_comments_count == factual_comments_count
    assert all((comment.text == COMMENT_TEXT, comment.author == author))
