# Copyright (c) 2013-2014 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""Subscribers adding mocked translation methods to render context, and request."""

from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.events import NewRequest

from pyramid_localize.tools import dummy_autotranslate


@subscriber(BeforeRender)
def global_renderer(event):
    """Add fake localizer, and translation methods to context."""
    request = event["request"]
    try:
        event["_"] = request._
    except AttributeError:
        event["_"] = dummy_autotranslate


@subscriber(NewRequest)
def add_localizer(event):
    """Add fake localizer and translation methods to request."""
    event.request._ = dummy_autotranslate
