import os

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

from core.testutils.mock_staticfiles import MockStaticfilesFinder


@override_settings(
    STATICFILES_DIRS=[
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'staticfiles'
        ),
    ]
)
class MockStaticfilesFinderTests(TestCase):
    @override_settings(STATICFILES_FINDERS=[])
    def test_no_finders_test_file_not_found(self):
        self.assertFalse(finders.find('icons/test.svg'))

    @override_settings(
        STATICFILES_FINDERS=[
            'django.contrib.staticfiles.finders.FileSystemFinder',
        ]
    )
    def test_filesystem_finder_finds_test_file(self):
        self.assertRegexpMatches(
            finders.find('icons/test.svg'),
            'icons/test.svg$'
        )

    @override_settings(
        STATICFILES_FINDERS=[
            'core.testutils.mock_staticfiles.MockStaticfilesFinder',
        ]
    )
    def test_mock_finder_no_setting_raises_improperlyconfigured(self):
        del settings.MOCK_STATICFILES_PATTERNS
        with self.assertRaises(ImproperlyConfigured):
            finders.find('icons/test.svg')

    @override_settings(
        STATICFILES_FINDERS=[
            'core.testutils.mock_staticfiles.MockStaticfilesFinder',
        ],
        MOCK_STATICFILES_PATTERNS=('this', 'should', 'be', 'a', 'dict')
    )
    def test_mock_finder_invalid_setting_raises_improperlyconfigured(self):
        with self.assertRaises(ImproperlyConfigured):
            finders.find('icons/test.svg')

    @override_settings(
        STATICFILES_FINDERS=[
            'core.testutils.mock_staticfiles.MockStaticfilesFinder',
        ],
        MOCK_STATICFILES_PATTERNS={
            'missing/*.svg': 'icons/test.svg',        
        }
    )
    def test_mock_finder_only_test_file_not_found(self):
        self.assertFalse(finders.find('missing/file.svg'))

    @override_settings(
        STATICFILES_FINDERS=[
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'core.testutils.mock_staticfiles.MockStaticfilesFinder',
        ],
        MOCK_STATICFILES_PATTERNS={
            'missing/*.svg': 'icons/test.svg',        
        }
    )
    def test_mock_finder_falls_back_to_filesystem_finder(self):
        self.assertRegexpMatches(
            finders.find('missing/file.svg'),
            'icons/test.svg$'
        )

    @override_settings(
        STATICFILES_FINDERS=[
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'core.testutils.mock_staticfiles.MockStaticfilesFinder',
        ],
        MOCK_STATICFILES_PATTERNS={
            'missing/*.svg': 'icons/test.svg',        
        }
    )
    def test_no_match_if_pattern_doesnt_match_input(self):
        self.assertFalse(finders.find('does-not-exist'))
