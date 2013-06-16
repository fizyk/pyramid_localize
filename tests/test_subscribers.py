# -*- coding: utf-8 -*-

import unittest
from mock import Mock


from pyramid import testing
from pyramid.request import Request
from pyramid.events import BeforeRender
from pyramid.events import NewRequest
from pyramid.i18n import Localizer

# for this tests, these will be imported internally by pyramid's config
# from pyramid_localize.subscribers.i18n import global_renderer
# from pyramid_localize.subscribers.i18n import add_localizer
# from pyramid_localize.subscribers.fake import global_renderer
# from pyramid_localize.subscribers.fake import add_localizer


class SubscribersTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _makeRequest(self, environ=None):
        if environ is None:
            environ = {}
        request = Request(environ)
        request.registry = self.config.registry

        return request

    def _makeBeforeRender(self, system, val=None):
        from pyramid.events import BeforeRender
        return BeforeRender(system, val)

    def test_i18n_new_request(self):
        '''i18n:Test new request'''
        self.config.scan('pyramid_localize.subscribers.i18n')
        request = self._makeRequest()
        request.registry.notify(NewRequest(request))
        self.assertTrue(isinstance(request.localizer, Localizer))
        self.assertTrue(hasattr(request, '_'))

    def test_i18n_before_render(self):
        '''i18n:Test before render'''
        self.config.scan('pyramid_localize.subscribers.i18n')
        request = self._makeRequest()
        before_render_event = self._makeBeforeRender({'request': request}, {})
        request.registry.notify(before_render_event)
        self.assertTrue('localizer' in before_render_event)
        self.assertTrue('_' in before_render_event)

    def test_i18n_before_render_and_request(self):
        '''i18n:Test before render with new request'''
        self.config.scan('pyramid_localize.subscribers.i18n')
        request = self._makeRequest()
        request.registry.notify(NewRequest(request))
        before_render_event = self._makeBeforeRender({'request': request}, {})
        request.registry.notify(before_render_event)
        self.assertTrue('localizer' in before_render_event)
        self.assertTrue('_' in before_render_event)

    def test_fake_new_request(self):
        '''fakei18n:Test new request'''
        self.config.scan('pyramid_localize.subscribers.fake')
        request = self._makeRequest()
        request.registry.notify(NewRequest(request))
        self.assertTrue(hasattr(request, '_'))

    def test_fake_before_render(self):
        '''fakei18n:Test before render'''
        self.config.scan('pyramid_localize.subscribers.fake')
        request = self._makeRequest()
        request.registry.notify(NewRequest(request))
        before_render_event = self._makeBeforeRender({'request': request}, {})
        request.registry.notify(before_render_event)
        self.assertTrue('_' in before_render_event)

    def test_fake_before_render_norequest(self):
        '''fakei18n:Test before render'''
        self.config.scan('pyramid_localize.subscribers.fake')
        request = self._makeRequest()
        before_render_event = self._makeBeforeRender({'request': request}, {})
        request.registry.notify(before_render_event)
        self.assertTrue('_' in before_render_event)
