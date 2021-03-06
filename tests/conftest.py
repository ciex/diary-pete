#!/usr/bin/env python
"""Test fixtures and utilities."""

# Copyright 2016 Vincent Ahrend

#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import pytest
import telegram

from peewee import SqliteDatabase
from random import randint
from telegram.ext import Updater
from playhouse.test_utils import test_database

from diary_peter.models import User, Record, Job

user_data = {
    'id': 4325497,
    'first_name': "Finz",
    'last_name': "Nilly",
    'username': "ululu",
    'type': "private"
}


@pytest.fixture(scope="module")
def test_db():
    """Provide an in-memory database for testing."""
    return SqliteDatabase(':memory:')


@pytest.fixture
def bot():
    """Fixture that returns a Telegram for Python bot object."""
    return telegram.Bot(os.environ.get('TG_TOKEN', None))


@pytest.fixture
def updater(request, scope="module"):
    """Fixture that returns a Telegram Bot updater object."""
    updater = Updater(os.environ.get("TG_TOKEN", False))

    def stop_updater():
        updater.stop()
    request.addfinalizer(stop_updater)

    return updater


@pytest.fixture
def tguser():
    """Fixture that returns a Telegram user object."""
    return telegram.User.de_json(user_data)


@pytest.fixture
def update():
    """Return a Telegram update object."""
    return custom_update()


@pytest.fixture
def user(test_db):
    """Return a single user object."""
    return create_users(test_db, num=1)[0]


def custom_update(msg="Lol I just ate a whole tuna."):
    """Return a custom update."""
    json = {
        'message_id': randint(40000, 50000),
        'from': user_data,
        'chat': user_data,
        'date': 1464350198,
        'text': msg
    }

    rv = telegram.Update.de_json({
        'update_id': randint(100000000, 200000000),
        'message': json
    })
    return rv


def inline_query(data):
    """Return a custom inline query."""
    iq = {
        'id': randint(40000, 50000),
        'from': user_data,
        'chat': user_data,
        'offset': 'a',
        'query': data
    }

    cq = {
        'id': randint(40000, 50000),
        'from': user_data,
        'message': {
            'message_id': randint(40000, 50000),
            'from': user_data,
            'chat': user_data,
            'date': 1464350198,
            'text': 'cq message text'
        },
        'data': data
    }

    rv = telegram.Update.de_json({
        'update_id': randint(100000000, 200000000),
        'inline_query': iq,
        'callback_query': cq
    })
    return rv


def create_users(db, num=10):
    """Utility func for creating users."""
    with test_database(db, [User, Record, Job], fail_silently=True):
        rv = []
        for i in range(num):
            rv.append(User.create_or_get(
                telegram_id=4325497 + i,
                name="User-{}".format(i),
                chat_id=4325497 + i
            )[0])
        return rv
