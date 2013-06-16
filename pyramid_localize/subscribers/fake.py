# -*- coding: utf-8 -*-

from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.events import NewRequest

from pyramid_localize.tools import dummy_autotranslate


@subscriber(BeforeRender)
def global_renderer(event):
    '''
        Subscriber, which extends variables available for renderer with translator method, and localizer object
    '''
    request = event['request']
    try:
        event['_'] = request._
    except AttributeError:
        event['_'] = dummy_autotranslate


@subscriber(NewRequest)
def add_localizer(event):
    '''
        We add localzer for each new request (we use tools.set_localizer method, as to not repeat yourself)
    '''

    event.request._ = dummy_autotranslate
