from dateutil import parser
from elasticsearch_dsl import A

from v1.documents import FilterablePagesDocument
from v1.util.ref import supported_languages


class OverviewSearchResults:
    def __init__(self, results):
        self.results = results
        self.aggs = results.aggregations

    @property
    def total_count(self):
        return self.results.hits.total.value

    @property
    def archived_count(self):
        return {
            b.key: b.doc_count for b in self.aggs.archived.buckets
        }.get('yes') or 0

    @property
    def category_choices(self):
        return [(b.key, b.key) for b in self.aggs.categories.buckets]

    @property
    def topic_choices(self):
        return [(b.key, b.key) for b in self.aggs.topics.buckets]

    @property
    def language_choices(self):
        language_codes = {b.key for b in self.aggs.languages.buckets}
        return [
            (k, v)
            for k, v in dict(supported_languages).items()
            if k in language_codes
        ]

    @property
    def min_date_published(self):
        return self._get_aggregate_date('min_date_published')

    @property
    def min_initial_filing_date(self):
        return self._get_aggregate_date('min_initial_filing_date')

    @property
    def min_start_dt(self):
        return self._get_aggregate_date('min_start_dt')

    def _get_aggregate_date(self, aggregate):
        value = getattr(self.aggs, aggregate).value
        if value:
            return parser.parse(value.value_as_string).date()


class FilterablePagesSearch:
    document_cls = FilterablePagesDocument

    def __init__(self, url_prefix=None, page_size=25):
        self.url_prefix = url_prefix or '/'
        self.page_size = page_size

    def search_overview(self):
        overview_search = self.get_overview_search()
        results = overview_search.execute()
        return OverviewSearchResults(results)

    def get_overview_search(self):
        search = self.document_cls.search()

        search = search.filter('prefix', url=self.url_prefix)

        search = search[:self.page_size]

        search.aggs.bucket(
            'categories',
            A('terms', field='categories.name', size=10000)
        )

        search.aggs.bucket('topics', A('terms', field='tags.slug', size=10000))

        search.aggs.bucket('languages', A('terms', field='language', size=100))

        search.aggs.bucket(
            'archived',
            A('terms', field='is_archived', size=10)
        )

        search.aggs.metric('min_start_date', A('min', field='start_dt'))

        return search
