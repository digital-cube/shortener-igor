# coding= utf-8
import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, Text, CHAR
from sqlalchemy.orm import relationship
import base.common.orm


class Url(base.common.orm.sql_base):

    __tablename__ = 'urls'

    id = Column(CHAR(10), primary_key=True)
    url = Column(Text, nullable=False)
    created = Column(DateTime, nullable=False)

    def __init__(self, _id, url):

        self.id = _id
        self.url = url
        self.created = datetime.datetime.now()


def main():
    pass


if __name__ == '__main__':

    main()
