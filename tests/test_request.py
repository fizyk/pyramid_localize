# -*- coding: utf-8 -*-


from sqlalchemy import create_engine
from pyramid.compat import text_type
from pyramid_basemodel import Base
from pyramid_basemodel import Session

from tests import BaseRequestTest
from pyramid_localize.models import Language
from pyramid_localize.request import locale_id
from pyramid_localize.request import locales


class RequestTest(BaseRequestTest):

    def test_request(self):
        '''Test whether route-parameters gets filled'''
        request = self._makeRequest()
        route_parameters = request.default_locale(slug='some-slug')
        self.assertTrue('__LOCALE__' in route_parameters)
        self.assertTrue(route_parameters['__LOCALE__'] in
                        request.config.localize.locales.available)

    def test_filled(self):
        '''Test whether correct __LOCALE__ is left'''
        request = self._makeRequest()
        route_parameters = request.default_locale(slug='some-slug', __LOCALE__='pl')
        self.assertEqual(route_parameters['__LOCALE__'], 'pl')

    def test_filled_wrong(self):
        '''Test whether wrong locale is change'''
        request = self._makeRequest()
        route_parameters = request.default_locale(slug='some-slug', __LOCALE__='fr')
        self.assertTrue(route_parameters['__LOCALE__'] in
                        request.config.localize.locales.available)

engine = create_engine('sqlite://', echo=False)
Session.configure(bind=engine)
Base.metadata.bind = engine


class RequestMethodTest(BaseRequestTest):

    def setUp(self):
        '''
            setUp test method @see unittest.TestCase.setUp
        '''
        Base.metadata.create_all(engine)

        for locale in ['pl', 'cz', 'fr']:
            locale_object = Language(name=text_type(locale),
                                     native_name=text_type(locale),
                                     language_code=text_type(locale))
            Session.add(locale_object)

    def tearDown(self):
        '''
            This tears tests down
        '''
        Base.metadata.drop_all(engine)

    def test_locale_id(self):
        '''Test for creating, and getting loacel id'''
        request = self._makeRequest()
        lid = locale_id(request)
        self.assertTrue(isinstance(lid, int))

    def test_locales(self):
        '''test return locales list'''
        request = self._makeRequest()
        locales_list = locales(request)
        self.assertEqual(3, len(locales_list))

    def test_locales_config(self):
        '''test return locales list limited by config'''
        request = self._makeRequest()
        locales_list = locales(request, True)
        self.assertEqual(4, len(locales_list))
