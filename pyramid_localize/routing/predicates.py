# -*- coding: utf-8 -*-


def language(field):
    def predicate(info, request):
        '''
            Checks whether language is one of the defaults
        '''
        if field in info['match'] and info['match'][field] in request.config.localize.locales.available:
            return True
        return False
    return predicate

language.__text__ = 'language predicate, to determine allowed languages in route'
