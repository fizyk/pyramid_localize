# -*- coding: utf-8 -*-

from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.events import NewRequest
from translationstring import _interp_regex


from pyramid.compat import text_type


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


def dummy_autotranslate(msgid, domain=None, default=None, mapping=None):
    '''
        Method that simulate autotranslate

        :param str msgid: Message or message id
        :param str domain: Translation domain
        :param str default: Default message
        :param dict mapping: Mapping dictionary for message variables

    '''
    # Try to return defaults first:
    tstr = None
    if default:
        tstr = default
    else:
        tstr = msgid

    if mapping and tstr:
        def replace(match):
            whole, param1, param2 = match.groups()
            return text_type(mapping.get(param1 or param2, whole))
        tstr = _interp_regex.sub(replace, tstr)

    return tstr
