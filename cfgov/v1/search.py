from datetime import date
from typing import NamedTuple

from dateutil import parser as parser
from elasticsearch_dsl import A

from v1.documents import FilterablePagesDocument
from v1.util.ref import supported_languages



def _es_dt_to_date(dt):
    return parser.parse(dt.value_as_string).date()


class SearchStats(NamedTuple):
    total_count: int
    archived_count: int
    language_choices: list
    topic_choices: list
    min_start_date: date
    max_start_date: date


class FilterablePagesSearch:
    def __init__(self, url_prefix=None):
        self.document = FilterablePagesDocument
        self.url_prefix = url_prefix or '/'

    def get_stats(self):
        results = self._get_stats_elasticsearch()
        aggs = results.aggregations

        stats = SearchStats()
        stats.total_count = results.hits.total.value

        stats.archived_count = {
            b.key: b.doc_count
            for b in
            stats.aggregations.archived.buckets
        }.get('yes') or 0

        language_codes = {b.key for b in aggs.languages.buckets}
        stats.language_choices = [
            (k, v) for k, v in dict(supported_languages).items()
            if k in language_codes
        ]

        # TODO: Query and use topic name for value instead of slug.
        stats.topic_choices = {b.key: b.key for b in aggs.topics.buckets}

        stats.min_start_date = _es_dt_to_date(aggs.min_start_date)
        stats.max_end_date = _es_dt_to_date(aggs.max_end_date)

        return stats

    def _get_stats_elasticsearch(self):
        search = self.document.search()

        search = search.filter('prefix', url=self.url_prefix)

        # search = search[0:10000]
        search = search[:0]

        # Aggregate languages in the result.
        search.aggs.bucket('languages', A('terms', field='language', size=100))

        # Aggregate topics in the result.
        search.aggs.bucket('topics', A('terms', field='tags.slug', size=10000))

        # Aggregate whether any archived pages exist in the result.
        search.aggs.bucket(
            'archived',
            A('terms', field='is_archived', size=10)
        )

        # Collect the earliest and latest post date.
        search.aggs.metric('min_start_date', A('min', field='start_dt'))
        search.aggs.metric('max_end_date', A('max', field='end_dt'))

        return search.execute()
