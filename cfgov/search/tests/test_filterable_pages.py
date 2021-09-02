from io import StringIO

from django.test import TestCase

from wagtail.core.models import Site

from search.elasticsearch_helpers import ElasticsearchTestsMixin
from search.filterable_pages import FilterablePagesSearch
from v1.models import LearnPage


class FilterablePagesSearchTests(ElasticsearchTestsMixin, TestCase):
    def test_overview_results_search_dsl(self):
        search = FilterablePagesSearch()
        overview_search = search.get_overview_search()

        self.assertEqual(overview_search.to_dict(), {
            'query': {
                'bool': {
                    'filter': [
                        {
                            'prefix': {
                                'url': '/',
                            },
                        },
                    ],
                },
            },
            'aggs': {
                'archived': {
                    'terms': {
                        'field': 'is_archived',
                        'size': 10,
                    },
                },
                'categories': {
                    'terms': {
                        'field': 'categories.name',
                        'size': 10000,
                    },
                },
                'languages': {
                    'terms': {
                        'field': 'language',
                        'size': 100,
                    },
                },
                'min_start_date': {
                    'min': {
                        'field': 'start_dt',
                    },
                }, 
                'topics': {
                    'terms': {
                        'field': 'tags.slug',
                        'size': 10000,
                    },
                },
            },
            'from': 0,
            'size': 25,
        }
    )

    def test_search_overview_no_results(self):
        self.rebuild_elasticsearch_index('v1', stdout=StringIO())
        search = FilterablePagesSearch()
        results = search.search_overview()
        
        self.assertEqual(results.total_count, 0)
        self.assertEqual(results.archived_count, 0)
        self.assertEqual(results.language_choices, [])
        self.assertEqual(results.topic_choices, [])
        self.assertEqual(results.category_choices, [])
        self.assertIsNone(results.min_filter_date)

    def test_search_overview_with_results(self):
        root_page = Site.objects.get(is_default_site=True).root_page

        page = LearnPage(title='Page', slug='page', live=True)
        page.categories.add(CFGOVPageCategory(name='Category 1'))
        page.categories.add(CFGOVPageCategory(name='Category 2'))
        page.tags.add('Tag 1')
        page.tags.add('Tag 2')
        page.language = 'en'
        root_page.add_child(instance=page)

        self.rebuild_elasticsearch_index('v1', stdout=StringIO())
        search = FilterablePagesSearch()
        results = search.search_overview()

        self.assertEqual(results.total_count, 1)
        self.assertEqual(results.archived_count, 0)
        self.assertEqual(results.language_choices, ['en'])
        self.assertEqual(results.topic_choices, ['tag-1', 'tag-2'])
        self.assertEqual(results.category_choices, ['Category 1', 'Category 2'])
        self.assertIsNone(results.min_start_date)
