# Copyright (c) 2013-2014 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""i18n subscribers."""

from pyramid.events import BeforeRender, NewRequest, subscriber

from pyramid_localize.tools import set_localizer


@subscriber(BeforeRender)
def global_renderer(event):
    """Add localizer, and translation methods to context."""
    request = event["request"]
    set_localizer(request)

    event["_"] = request._
    event["localizer"] = request.localizer


@subscriber(NewRequest)
def add_localizer(event):
    """Add localizer and translation methods to request."""
    set_localizer(event.request)
