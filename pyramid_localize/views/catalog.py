# -*- coding: utf-8 -*-
import sys
import os
import time
import logging
import subprocess


from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.asset import resolve_asset_spec
from pyramid.path import package_path
from pyramid.httpexceptions import HTTPFound

from pyramid_localize.tools import destination_path
from pyramid_localize.tools import set_localizer

logger = logging.getLogger(__name__)


@view_defaults(permission='manage_translations')
class CatalogView(object):

    '''
            Class for all translation views
    '''

    def __init__(request):
        '''Assign request'''
        self.request = request

    def _translation_file(self, language, domain, extension='po'):
        '''
            Creates a translation file path

            :param str language: two-letetr language code
            :param str domain: translation domain name
            :param str extension: translation file extension (po/mo)
        '''

        translation_destination = destination_path(self.request)
        return os.path.join(translation_destination, language, 'LC_MESSAGES', domain + '.' + extension)

    def _translation_template_path(self, spec):
        '''
            calculates path to translation template file

            :param str spec: either full path, or package related path
        '''
        # resolving possible asset spec to path (pyramid way):
        package_name, filename = resolve_asset_spec(spec)
        if package_name is None:  # absolute filename
            return filename
        else:
            __import__(package_name)
            package = sys.modules[package_name]
            return os.path.join(package_path(package), filename)

    @view_config(route_name='localize:index', renderer='pyramid_localize:resources/templates/index.mako')
    def index(self):
        '''
            Simple action to return list of files, and list of domains (preferably with additional data, like compilation date, .po creation date)
        '''
        translations = {}
        translation_sources = self.request.config.i18n.translation.sources

        for language in self.request.config.i18n.available_languages:
            translations[language] = {}
            for domain in translation_sources:
                translations[language][domain] = {
                    'po': None,
                    'pot': None,
                    'mo': None
                }
                po_file = self._translation_file(language, domain)
                if os.path.isfile(po_file):
                    translations[language][domain]['po'] = time.ctime(os.path.getmtime(po_file))

                pot_file = self._translation_template_path(translation_sources[domain])
                if os.path.isfile(pot_file):
                    translations[language][domain]['pot'] = time.ctime(os.path.getmtime(pot_file))

                mo_file = self._translation_file(language, domain, 'mo')
                if os.path.isfile(mo_file):
                    translations[language][domain]['mo'] = time.ctime(os.path.getmtime(mo_file))

        return {'translations': translations}

    @view_config(route_name='localize:update', renderer='pyramid_localize:resources/templates/index.mako')
    def update_catalog(self):
        '''
            This action updates or initializes catalogs
        '''
        data = self.index()
        translation_sources = self.request.config.i18n.translation.sources

        for domain in translation_sources:

            pot_file = self._translation_template_path(translation_sources[domain])

            if not os.path.isfile(pot_file):
                logger.critical('pot file for {domain} does not exists!'.format(domain=domain))

            for language in self.request.config.i18n.available_languages:
                po_file = self._translation_file(language, domain)
                if os.path.isfile(po_file):
                    logger.debug('po file for {domain}, {language} exists, proceeding with update'.format(
                        domain=domain, language=language))
                    if subprocess.call([self.request.config.i18n.pybabel,
                                        'update',
                                        '-l', language,
                                        '-i', pot_file,
                                        '-o', po_file,
                                        '--previous']):
                        logger.error('Error while trying to update {po} file!'.format(po=po_file))
                else:
                    logger.debug('po file for {domain}, {language} does not exists, proceeding with initialize'.format(
                        domain=domain, language=language))
                    if subprocess.call([self.request.config.i18n.pybabel,
                                        'init',
                                        '-l', language,
                                        '-i', pot_file,
                                        '-o', po_file]):
                        logger.error('Error while trying to update {po} file!'.format(po=po_file))

        return HTTPFound(location=self.request.route_url('localize:index'))

    @view_config(route_name='localize:compile', renderer='pyramid_localize:resources/templates/index.mako')
    def compile_catalog(self):
        '''
            This action compiles catalogs
        '''
        data = self.index()
        translation_sources = self.request.config.i18n.translation.sources

        for domain in translation_sources:

            for language in self.request.config.i18n.available_languages:
                po_file = self._translation_file(language, domain)
                mo_file = self._translation_file(language, domain, 'mo')
                if os.path.isfile(po_file):
                    logger.debug('po file for {domain}, {language} exists, proceeding with compilation'.format(
                        domain=domain, language=language))
                    if subprocess.call([self.request.config.i18n.pybabel,
                                        'compile',
                                        '-l', language,
                                        '-i', po_file,
                                        '-o', mo_file,
                                        '--use-fuzzy']):
                        logger.error('Error while trying to compile {po} file!'.format(po=po_file))

        return HTTPFound(location=self.request.route_url('localize:index'))

    @view_config(route_name='localize:reload', xhr='True', renderer='json')
    @view_config(route_name='localize:reload', renderer='pyramid_localize:resources/templates/index.mako')
    def reload_catalog(self):
        '''
            This action is responsible for reloading catalogs
        '''
        data = self.index()
        translation_sources = self.request.config.i18n.translation.sources

        set_localizer(self.request, True)

        if self.request.is_xhr:
            return {'status': True, 'msg': self.request._('Localizators has been reloaded')}

        return HTTPFound(location=self.request.route_url('localize:index'))
