# Copyright (c) 2013-2014 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""Language model."""

import gettext
from datetime import datetime
from typing import Any

import pycountry
from pyramid_basemodel import Base
from sqlalchemy import DateTime, Integer, Sequence, String, Unicode, event, func
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapped, Mapper, mapped_column


class Language(Base):
    """Language table model definition."""

    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(Integer, Sequence(__tablename__ + "_sq"), primary_key=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(Unicode(45), nullable=False)
    native_name: Mapped[str] = mapped_column(Unicode(45), nullable=False)
    language_code: Mapped[str] = mapped_column(String(2), unique=True, nullable=False)  # ISO 639-1 (Alpha2)

    def __str__(self) -> str:  # pragma: no cover
        """Language to string conversion."""
        return self.name


@event.listens_for(Language, "before_insert")
def before_language_insert(_: Mapper[Any], __: Connection, language: Language) -> None:
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
        lang_locale = gettext.translation("iso639-3", pycountry.LOCALES_DIR, languages=[language.language_code])
        localize = lang_locale.gettext

        language.native_name = str(localize(lang_data.name))
