# Copyright (c) 2013-2014 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""Language model."""
import gettext


from sqlalchemy import Column
from sqlalchemy import Sequence
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import event
from pyramid_basemodel import Base
import pycountry


class Language(Base):
    """Language table model definition."""

    __tablename__ = "languages"

    id = Column(Integer, Sequence(__tablename__ + "_sq"), primary_key=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    name = Column(Unicode(45), nullable=False)
    native_name = Column(Unicode(45), nullable=False)
    language_code = Column(String(2), unique=True, nullable=False)  # ISO 639-1 (Alpha2)

    def __unicode__(self):  # pragma: no cover
        """Language to unicode conversion."""
        return self.name

    def __str__(self):  # pragma: no cover
        """Language to string conversion."""
        return self.name.encode("utf8")


@event.listens_for(Language, "before_insert")
def before_language_insert(_, __, language):
    """Set name and native_name before creation."""
    # Check language code
    lang_data = pycountry.languages.get(alpha_2=language.language_code)
    if lang_data is None:
        # Language code not recognized, set defaults
        language.name = "UNKNOWN"
        language.native_name = "UNKNOWN"
        return

    # Set name and native_name
    language.name = str(lang_data.name)

    if language.language_code == "en":
        # English does not have a translation file
        language.native_name = str(lang_data.name)

    else:
        lang_locale = gettext.translation("iso639_3", pycountry.LOCALES_DIR, languages=[language.language_code])
        localize = lang_locale.gettext

        language.native_name = str(localize(lang_data.name))
