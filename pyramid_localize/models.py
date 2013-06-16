# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import Sequence
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import DateTime
from sqlalchemy import func

from pyramid_basemodel import Base


class Language(Base):

    '''
        languages table model definition
    '''

    __tablename__ = 'languages'

    id = Column(Integer, Sequence(__tablename__ + '_sq'), primary_key=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    name = Column(Unicode(45), nullable=False)
    native_name = Column(Unicode(45), nullable=False)
    language_code = Column(String(2), unique=True, nullable=False)  # ISO 639-1 (Alpha2)

    def __unicode__(self):  # pragma: no cover
        '''
            Language to unicode conversion
        '''
        return self.name

    def __str__(self):  # pragma: no cover
        '''
            Language to string conversion
        '''
        return self.name.encode('utf8')
