# -*- coding: utf-8 -*-

import unittest


from pyramid_localize.tools import dummy_autotranslate


class DummyTranslationTests(unittest.TestCase):

    def test_message(self):
        '''dummy_autotranslate::simple'''
        text = 'Simple fake text'
        translated_text = dummy_autotranslate(text)
        self.assertEqual(text, translated_text)

    def test_default(self):
        '''dummy_autotranslate::default'''
        text = 'Simple fake text'
        translated_text = dummy_autotranslate('test-msgid', default=text)
        self.assertEqual(text, translated_text)

    def test_replace(self):
        '''dummy_autotranslate::default'''
        text = 'Simple ${what} text'
        translated_text = dummy_autotranslate(text, mapping={'what': 'fake'})
        self.assertEqual('Simple fake text', translated_text)
