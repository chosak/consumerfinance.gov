from html import unescape
from operator import itemgetter

from django.core.exceptions import FieldDoesNotExist
from django.utils.html import strip_tags

from django_opensearch_dsl import Document, fields
from django_opensearch_dsl.registries import registry
from opensearchpy.helpers.query import MultiMatch

from search.elasticsearch_helpers import environment_specific_index
from v1.models.blog_page import BlogPage, LegacyBlogPage
from v1.models.enforcement_action_page import EnforcementActionPage
from v1.models.learn_page import (
    AbstractFilterPage,
    DocumentDetailPage,
    EventPage,
    LearnPage,
)
from v1.models.newsroom_page import LegacyNewsroomPage, NewsroomPage


@registry.register_document
class FilterablePagesDocument(Document):
    model_class = fields.KeywordField()

    path = fields.KeywordField()
    depth = fields.IntegerField()
    title = fields.TextField(fields={"raw": fields.KeywordField()})

    start_date = fields.DateField()
    end_date = fields.DateField()
    language = fields.KeywordField()

    tags = fields.ObjectField(
        properties={"slug": fields.KeywordField(), "name": fields.TextField()}
    )
    categories = fields.ObjectField(properties={"name": fields.KeywordField()})

    statuses = fields.KeywordField()
    products = fields.KeywordField()
    content = fields.TextField()
    preview_title = fields.TextField()
    preview_subheading = fields.TextField()
    preview_description = fields.TextField()

    def get_queryset(self, *args, **kwargs):
        return AbstractFilterPage.objects.live().public().specific()

    def prepare_model_class(self, instance):
        return instance.__class__.__name__

    def prepare_start_date(self, instance):
        return getattr(instance, instance.__class__.start_date_field)

    def prepare_end_date(self, instance):
        if hasattr(instance.__class__, "end_date_field"):
            return getattr(instance, instance.__class__.end_date_field)
        else:
            return self.prepare_start_date(instance)

    def prepare_statuses(self, instance):
        statuses = getattr(instance, "statuses", None)
        if statuses is not None:
            return [status.status for status in statuses.all()]
        else:
            return None

    def prepare_products(self, instance):
        products = getattr(instance, "products", None)
        if products is not None:
            return [p.product for p in products.all()]
        else:
            return None

    def prepare_content(self, instance):
        try:
            content_field = instance._meta.get_field("content")
            value = content_field.value_from_object(instance)
            content = content_field.get_searchable_content(value)
            content = content.pop()
            return content
        except FieldDoesNotExist:
            return None
        except IndexError:
            return None

    def prepare_preview_description(self, instance):
        return unescape(strip_tags(instance.preview_description))

    def get_instances_from_related(self, related_instance):
        # Related instances all inherit from AbstractFilterPage.
        return related_instance

    class Django:
        model = AbstractFilterPage

        related_models = [
            BlogPage,
            DocumentDetailPage,
            EnforcementActionPage,
            EventPage,
            LearnPage,
            LegacyBlogPage,
            LegacyNewsroomPage,
            NewsroomPage,
        ]

    class Index:
        name = environment_specific_index("filterable-pages")
        settings = {"index.max_ngram_diff": 23}
        auto_refresh = False


class FilterablePagesSearch:
    def __init__(
        self,
        root_page,
        children_only=True,
        ordering=None,
        aggregate_bucket_count=1000,
        **kwargs,
    ):
        search = self._get_base_search(root_page, children_only)

        search = self._filter_search(search, **kwargs)

        search = self._add_search_aggregates(search, aggregate_bucket_count)

        if ordering:
            search = search.sort(ordering)

        # We only care about retrieving the ID field because we're going to
        # query the database to retrieve the full Django models anyway.
        search = search.source(excludes=["*"])

        self.search = search
        self.results = None

    def __getitem__(self, key):
        if self.results is None:
            if isinstance(key, slice):
                self.search = self.search[key]
                return self

            self._execute()

        return self.results[key]

    def __len__(self):
        self._execute()

        return sum(
            map(
                itemgetter("doc_count"),
                self.response.aggs.language_codes.buckets,
            )
        )

    def _execute(self):
        if self.results is None:
            results = self.search.execute()
            self._validate_search_aggregates(results)
            self.results = results

    @classmethod
    def _get_base_search(cls, root_page, children_only):
        search = FilterablePagesDocument.search()

        search = search.filter("prefix", path=root_page.path)

        if children_only:
            search = search.filter("term", depth=root_page.depth + 1)
        else:
            search = search.filter("range", depth={"gt": root_page.depth})

        return search

    @classmethod
    def _filter_search(cls, search, **kwargs):
        # Filter by query, if specified.
        # This comes in as kwarg "title" for backwards-compatibility reasons.
        search = cls._query(search, kwargs.get("title"))

        # Add any date-based filtering.
        search = cls._filter_by_date(
            search, kwargs.get("from_date"), kwargs.get("to_date")
        )

        # Add any other supported filters.
        for kwarg, filter_by in (
            ("model_class", "model_class"),
            ("language", "language"),
            ("topics", "tags__slug"),
            ("categories", "categories__name"),
            ("statuses", "statuses"),
            ("products", "products"),
        ):
            search = cls._filter_by_terms(search, filter_by, kwargs.get(kwarg))

        return search

    @classmethod
    def _query(cls, search, q):
        if q:
            query = MultiMatch(
                query=q,
                fields=[
                    "title^10",
                    "tags.name^10",
                    "content",
                    "preview_title",
                    "preview_subheading",
                    "preview_description",
                ],
                type="phrase_prefix",
                slop=2,
            )

            search = search.query(query)

        return search

    @classmethod
    def _filter_by_date(cls, search, from_date, to_date):
        if from_date and to_date:
            ranges = [
                {"end_date": {"gte": from_date}},
                {"start_date": {"lte": to_date}},
            ]
        elif from_date:
            ranges = [{"end_date": {"gte": from_date}}]
        elif to_date:
            ranges = [{"start_date": {"lte": to_date}}]
        else:
            ranges = []

        for range in ranges:
            search = search.filter("range", **range)

        return search

    @classmethod
    def _filter_by_terms(cls, search, filter_by, values):
        if values:
            if isinstance(values, str):
                values = [values]

            search = search.filter("terms", **{filter_by: values})

        return search

    @classmethod
    def _add_search_aggregates(cls, search, bucket_count):
        # When computing terms bucket aggregates in OpenSearch or Elasticsearch,
        # it's necessary to specify the maximum number of buckets to compute:
        #
        # https://opensearch.org/docs/latest/aggregations/bucket-agg/#terms
        #
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#search-aggregations-bucket-terms-aggregation-size
        #
        # We can specify a large value for this and then check the result of
        # the aggregation to ensure that we haven't exceeded the maximum.

        # Aggregate unique language codes in the result.
        search.aggs.bucket(
            "language_codes",
            "terms",
            field="language",
            size=bucket_count,
        )

        # Aggregate unique tag slugs in the result.
        search.aggs.bucket(
            "tag_slugs",
            "terms",
            field="tags.slug",
            size=bucket_count,
        )

        # Determine the earliest page date.
        search.aggs.metric("min_start_date", "min", field="start_date")

        return search

    def _validate_aggregates(self, results):
        # We check the computed aggregates to ensure that we provided a
        # sufficient number of buckets to hold all of the unique terms.
        #
        # Both OpenSearch and Elasticsearch provide a "sum_other_doc_count"
        # value as a way to check this:
        #
        # https://opensearch.org/docs/latest/aggregations/bucket-agg/#terms
        #
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#terms-agg-doc-count-error
        if any(
            getattr(bucket, "sum_other_doc_count", None)
            for bucket in results.aggs
        ):
            raise RuntimeError(
                f"Aggregation exceeded bucket count: {results.aggs.to_dict()}"
            )

    class SearchResults:
        def __init__(self, response):
            self.response = response

        def __bool__(self):
            return bool(self.response)

        def __len__(self):
            return sum(
                map(
                    itemgetter("doc_count"),
                    self.response.aggs.language_codes.buckets,
                )
            )

        def __getitem__(self, key):
            self.response = self.response._search[key]
            return self.response._search[key]

        def to_queryset(self):
            return self.response.to_queryset()

        @property
        def language_codes(self):
            return [b.key for b in self.response.aggs.language_codes.buckets]

        @property
        def tag_slugs(self):
            return [b.key for b in self.response.aggs.tag_slugs.buckets]

        @property
        def min_start_date(self):
            return (
                FilterablePagesDocument._fields["start_date"]
                .deserialize(self.response.aggs.min_start_date.value_as_string)
                .date()
            )
