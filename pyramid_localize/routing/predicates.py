# -*- coding: utf-8 -*-

# Copyright (c) 2013 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT


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
