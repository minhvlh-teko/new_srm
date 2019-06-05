# coding=utf-8
import logging

import pytest

__author__ = 'Kien'
_logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def app(request):
    from srm import app
    from srm.models import db
    # print("Start app and init db.......")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    # test db initializations go below here
    db.create_all()

    def teardown():
        # print("Tear down db")
        db.session.remove()
        db.drop_all()
        ctx.pop()

    request.addfinalizer(teardown)
    return app
