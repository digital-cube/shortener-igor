# coding= utf-8

from base.application.components import Base
from base.application.components import api
from base.application.components import params
from base.application.components import authenticated
from sqlalchemy import desc

import datetime
import decimal
import json
import base.common.orm
from src.models.shortener import Url
import random

@api(
    URI='/short/:id',
)
class Short(Base):
    @params(
        {'name': 'id', 'type': str, 'doc': 'id', 'required': True},
    )
    def get(self, _id):

        session = base.common.orm.orm.session()
        db_url = session.query(Url).filter(Url.id == _id).one_or_none()

        if not db_url:
            return self.error("not found")

        return self.ok({'url': db_url.url})

@api(
    URI='/r/:id',
    PREFIX='',
)
class Redirect(Base):
    @params(
        {'name': 'id', 'type': str, 'doc': 'id', 'required': True},
    )
    def get(self, _id):

        session = base.common.orm.orm.session()
        db_url = session.query(Url).filter(Url.id == _id).one_or_none()

        if not db_url:
            return self.error("not found")

        self.redirect(db_url.url)

        return



@api(
    URI='/admin/last',

)
class AdminLast(Base):
    @params(
        {'name': 'limit', 'type': int, 'doc': 'url', 'required': True},
    )
    def get(self, limit):
        session = base.common.orm.orm.session()

        ret = []
        for i in session.query(Url).order_by(desc(Url.created)).limit(limit).all():
            ret.append([i.id, i.url, str(i.created)])

        return self.ok({'list':ret})


@api(
    URI='/',
    PREFIX=False

)
class Index(Base):
    def get(self):
        self.render('OLDindex.html')


@api(
    URI='/short',

)
class ShortCreate(Base):
    @params(
        {'name': 'url', 'type': str, 'doc': 'url', 'required': True},
    )
    def put(self, url):

        session = base.common.orm.orm.session()

        for retries in range(0,10):
            _id = str(random.randint(1000000,9999999))
            exists = session.query(Url).filter(Url.id == _id).one_or_none()
            if not exists:
                break

        if exists:
            return self.error("Error creating unique id in 10 retries")

        db_url = Url(_id, url)
        session.add(db_url)

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            return self.error("DB problem")

        return self.ok({"id": _id})

