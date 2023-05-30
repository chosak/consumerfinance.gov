import json
from datetime import date, datetime
from io import StringIO
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from wagtail.models import Page

from dateutil.relativedelta import relativedelta

from core.testutils.test_cases import WagtailPageTreeTestCase
from search.elasticsearch_helpers import ElasticsearchTestsMixin
from v1.documents import FilterablePagesDocument, FilterablePagesSearch
from v1.models import (
    AbstractFilterPage,
    BlogPage,
    CFGOVPageCategory,
    DocumentDetailPage,
    EnforcementActionPage,
    EnforcementActionProduct,
    EnforcementActionStatus,
    EventPage,
    SublandingFilterablePage,
)


class FilterablePagesDocumentTest(TestCase):
    def test_model_class_added(self):
        self.assertEqual(
            FilterablePagesDocument.django.model, AbstractFilterPage
        )

    def test_ignore_signal_default(self):
        self.assertFalse(FilterablePagesDocument.django.ignore_signals)

    def test_auto_refresh_default(self):
        self.assertFalse(FilterablePagesDocument.Index.auto_refresh)

    def test_fields_populated(self):
        mapping = FilterablePagesDocument._doc_type.mapping
        self.assertCountEqual(
            mapping.properties.properties.to_dict().keys(),
            [
                "model_class",
                "path",
                "depth",
                "title",
                "start_date",
                "end_date",
                "language",
                "tags",
                "categories",
                "statuses",
                "products",
                "content",
                "preview_title",
                "preview_subheading",
                "preview_description",
            ],
        )

    def test_get_queryset(self):
        test_event = EventPage(title="Testing", start_dt=timezone.now())
        qs = FilterablePagesDocument().get_queryset()
        self.assertFalse(qs.filter(title=test_event.title).exists())

    def test_prepare_start_and_end_dates(self):
        document = FilterablePagesDocument()

        ddp = DocumentDetailPage(date_published=date(2023, 1, 1))
        ddp_data = document.prepare(ddp)
        self.assertEqual(ddp_data["start_date"], ddp.date_published)
        self.assertEqual(ddp_data["end_date"], ddp.date_published)

        eap = EnforcementActionPage(
            date_published=date(2023, 1, 1),
            initial_filing_date=date(2022, 12, 1),
        )
        eap_data = document.prepare(eap)
        self.assertEqual(eap_data["start_date"], eap.initial_filing_date)
        self.assertEqual(eap_data["end_date"], eap.initial_filing_date)

        ep = EventPage(
            date_published=date(2023, 1, 1),
            start_dt=datetime(2023, 2, 1),
            end_dt=datetime(2023, 2, 2),
        )
        ep_data = document.prepare(ep)
        self.assertEqual(ep_data["start_date"], ep.start_dt)
        self.assertEqual(ep_data["end_date"], ep.end_dt)

    def test_prepare_statuses(self):
        enforcement = EnforcementActionPage(
            title="Great Test Page",
            preview_description="This is a great test page.",
            initial_filing_date=timezone.now(),
        )
        status = EnforcementActionStatus(status="expired-terminated-dismissed")
        enforcement.statuses.add(status)
        doc = FilterablePagesDocument()
        prepared_data = doc.prepare(enforcement)
        self.assertEqual(
            prepared_data["statuses"], ["expired-terminated-dismissed"]
        )

    def test_prepare_content_no_content_defined(self):
        event = EventPage(title="Event Test", start_dt=timezone.now())
        doc = FilterablePagesDocument()
        prepared_data = doc.prepare(event)
        self.assertIsNone(prepared_data["content"])

    def test_prepare_content_exists(self):
        blog = BlogPage(
            title="Test Blog",
            preview_title="Blog for Testing",
            content=json.dumps(
                [
                    {
                        "type": "full_width_text",
                        "value": [
                            {
                                "type": "content",
                                "value": "Blog Text",
                            },
                        ],
                    },
                ]
            ),
        )
        doc = FilterablePagesDocument()
        prepared_data = doc.prepare(blog)
        self.assertEqual(prepared_data["content"], "Blog Text")

    def test_prepare_content_empty(self):
        blog = BlogPage(title="Test Blog", content=json.dumps([]))
        doc = FilterablePagesDocument()
        prepared_data = doc.prepare(blog)
        self.assertIsNone(prepared_data["content"])

    def test_prepare_products(self):
        enforcement = EnforcementActionPage(
            title="Great Test Page",
            preview_description="This is a great test page.",
            initial_filing_date=timezone.now(),
        )
        product = EnforcementActionProduct(product="Fair Lending")
        enforcement.products.add(product)
        doc = FilterablePagesDocument()
        prepared_data = doc.prepare(enforcement)
        self.assertEqual(prepared_data["products"], ["Fair Lending"])


class ElasticsearchWagtailPageTreeTestCase(
    ElasticsearchTestsMixin, WagtailPageTreeTestCase
):
    """Test case that creates and indexes a Wagtail page tree."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.rebuild_elasticsearch_index(
            FilterablePagesDocument.Index.name, stdout=StringIO()
        )


def add_to_page(slug, field, value):
    page = Page.objects.get(slug=slug).specific
    getattr(page, field).add(value)
    page.save()


class FilterableSearchTests(ElasticsearchWagtailPageTreeTestCase):
    @classmethod
    def get_page_tree(cls):
        return [
            (
                SublandingFilterablePage(title="search1"),
                [
                    DocumentDetailPage(
                        title="child1",
                        language="en",
                        date_published=date(2023, 1, 1),
                    ),
                    DocumentDetailPage(
                        title="child2",
                        language="es",
                        date_published=date(2023, 1, 2),
                        preview_title="2child",
                        preview_subheading="2child2",
                    ),
                    (
                        SublandingFilterablePage(title="search2"),
                        [
                            DocumentDetailPage(title="nested child1"),
                            DocumentDetailPage(title="nested child2"),
                        ],
                    ),
                ],
            )
        ]

    @classmethod
    def build_page_tree(cls, page_tree):
        tree = super().build_page_tree(page_tree)

        # Tags need to be added to pages after they've already been saved.
        add_to_page("child1", "tags", "foo")
        add_to_page("child2", "tags", "bar")

        return tree

    def test_search_root_without_aggregates(self):
        # By default search only returns AbstractFilterPages
        # that are direct children of the specified root.
        search = FilterablePagesSearch(self.page_tree[0])
        results = search.search()

        self.assertEqual(len(results), 2)
        self.assertIsNone(results.min_start_date)
        self.assertIsNone(results.language_codes)
        self.assertIsNone(results.tag_slugs)

    def test_search_root_with_aggregates(self):
        search = FilterablePagesSearch(self.page_tree[0])
        results = search.search(include_aggregates=True)

        self.assertEqual(len(results), 2)
        self.assertEqual(results.min_start_date, date(2023, 1, 1))
        self.assertEqual(results.language_codes, ["en", "es"])
        self.assertEqual(results.tag_slugs, ["bar", "foo"])

    def test_search_root_with_aggregates_insufficient_buckets(self):
        search = FilterablePagesSearch(self.page_tree[0])
        with self.assertRaises(RuntimeError) as e:
            search.search(include_aggregates=True, aggregate_bucket_count=1)

        self.assertIn("Aggregation exceeded bucket count", str(e.exception))

    def test_search_results_slicing(self):
        search = FilterablePagesSearch(self.page_tree[0])
        results = search.search()

        child1 = AbstractFilterPage.objects.get(slug="child1")

        first = results[0]
        self.assertEqual(first, child1)

        sliced = results[:1]
        self.assertEqual(sliced.count(), 1)
        self.assertQuerysetEqual(sliced, [child1])

    def test_search_children_only(self):
        # Setting children_only to False returns all AbstractFilterablePages
        # that live anywhere underneath the specified root.
        search = FilterablePagesSearch(self.page_tree[0], children_only=False)
        results = search.search()

        self.assertEqual(len(results), 4)

    def test_search_from_other_page(self):
        # Search works starting from some other page in the tree.
        page = Page.objects.get(slug="search2")
        search = FilterablePagesSearch(page)
        results = search.search()

        self.assertEqual(len(results), 2)

    def test_search_by_title(self):
        search = FilterablePagesSearch(self.page_tree[0], children_only=False)

        self.assertEqual(len(search.search(title="child")), 4)
        self.assertEqual(len(search.search(title="child1")), 2)
        self.assertFalse(search.search(title="child3"))

    def test_search_by_preview_title(self):
        search = FilterablePagesSearch(self.page_tree[0], children_only=False)

        results_title = search.search(title="child2")
        self.assertEqual(len(results_title), 2)

        results_preview_title = search.search(title="2child")
        self.assertEqual(len(results_preview_title), 1)

    def test_search_by_preview_subheading(self):
        search = FilterablePagesSearch(self.page_tree[0], children_only=False)
        results_preview_subheading = search.search(title="2child2")
        self.assertEqual(len(results_preview_subheading), 1)

    def test_search_results_bool(self):
        search = FilterablePagesSearch(self.page_tree[0])
        self.assertTrue(search.search(title="child"))
        self.assertFalse(search.search(title="dlihc"))


class FilterableSearchFilteringTests(ElasticsearchWagtailPageTreeTestCase):
    @classmethod
    def get_page_tree(cls):
        cls.now = timezone.now()
        cls.today = cls.now.date()
        cls.yesterday = cls.today - relativedelta(days=1)

        return [
            (
                SublandingFilterablePage(title="search"),
                [
                    BlogPage(
                        title="blog1",
                        language="en",
                        date_published=cls.today,
                    ),
                    BlogPage(
                        title="blog2",
                        language="es",
                        date_published=cls.yesterday,
                    ),
                    EnforcementActionPage(title="enforcement1"),
                    EnforcementActionPage(title="enforcement2"),
                    EventPage(title="event1", start_dt=cls.now),
                    EventPage(title="event2", start_dt=cls.now),
                ],
            ),
        ]

    @classmethod
    def build_page_tree(cls, page_tree):
        tree = super().build_page_tree(page_tree)

        # Page tags, categories, products, and statuses can't be set at
        # creation time, so they need to be added after the page tree
        # has been created.
        add_to_page("blog1", "tags", "foo")
        add_to_page("blog1", "categories", CFGOVPageCategory(name="foo"))
        add_to_page("blog2", "tags", "bar")
        add_to_page("blog2", "categories", CFGOVPageCategory(name="bar"))
        add_to_page(
            "enforcement1",
            "products",
            EnforcementActionProduct(product="Debt Collection"),
        )
        add_to_page(
            "enforcement2",
            "statuses",
            EnforcementActionStatus(status="expired-terminated-dismissed"),
        )

        return tree

    def test_no_filters(self):
        search = FilterablePagesSearch(self.page_tree[0])
        results = search.search()
        self.assertEqual(len(results), 6)

    def test_ordering_default(self):
        search = FilterablePagesSearch(self.page_tree[0])
        results = search.search()
        self.assertEqual(
            results[0],
            AbstractFilterPage.objects.get(slug="blog1"),
        )

    def test_ordering_custom(self):
        search = FilterablePagesSearch(
            self.page_tree[0], ordering="-title.raw"
        )
        results = search.search()
        self.assertEqual(
            results[0],
            AbstractFilterPage.objects.get(slug="event2"),
        )

    def test_filter_by_language(self):
        search = FilterablePagesSearch(self.page_tree[0])
        results = search.search(language="es")
        self.assertEqual(len(results), 1)

    def test_filter_by_date(self):
        search = FilterablePagesSearch(self.page_tree[0])
        results = search.search(from_date=self.today, to_date=self.today)
        self.assertEqual(len(results), 1)

        results = search.search(
            from_date=self.yesterday, to_date=self.yesterday
        )
        self.assertEqual(len(results), 1)

        results = search.search(from_date=self.today)
        self.assertEqual(len(results), 1)

        results = search.search(to_date=self.yesterday)
        self.assertEqual(len(results), 1)

    def test_filter_by_topics(self):
        search = FilterablePagesSearch(self.page_tree[0])
        results = search.search(topics=["foo"])
        self.assertEqual(len(results), 1)

        results = search.search(topics=["bad"])
        self.assertFalse(results)

    def test_filter_by_categories(self):
        search = FilterablePagesSearch(self.page_tree[0])
        results = search.search(categories=["bar"])
        self.assertEqual(len(results), 1)

        results = search.search(categories=["bad"])
        self.assertFalse(results)

    def test_filter_by_class(self):
        search = FilterablePagesSearch(self.page_tree[0])
        results = search.search(model_class=EventPage.__name__)
        self.assertEqual(len(results), 2)

    def test_filter_by_products(self):
        search = FilterablePagesSearch(self.page_tree[0])

        results = search.search(products=["Debt Collection"])
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].specific,
            EnforcementActionPage.objects.get(slug="enforcement1"),
        )

        results = search.search(products=["bad"])
        self.assertFalse(results)

    def test_filter_by_statuses(self):
        search = FilterablePagesSearch(self.page_tree[0])

        results = search.search(statuses=["expired-terminated-dismissed"])
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].specific,
            EnforcementActionPage.objects.get(slug="enforcement2"),
        )

        results = search.search(statuses=["bad"])
        self.assertFalse(results)


class TestThatWagtailPageSignalsUpdateIndex(
    ElasticsearchWagtailPageTreeTestCase
):
    @classmethod
    def get_page_tree(cls):
        return [
            (
                BlogPage(title="parent", live=True),
                [
                    BlogPage(title="blog1", live=True),
                    BlogPage(title="blog2", live=True),
                    BlogPage(title="blog3", live=True),
                ],
            ),
        ]

    def test_signals_update_index(self):
        root = self.page_tree[0]
        blog1 = BlogPage.objects.get(slug="blog1")
        blog2 = BlogPage.objects.get(slug="blog2")
        blog3 = BlogPage.objects.get(slug="blog3")

        search = FilterablePagesSearch(self.page_tree[0])

        # Initially a search at the root should return 3 results.
        results = search.search(title="blog")
        self.assertEqual(len(results), 3)

        # By default we set OPENSEARCH_DSL_AUTOSYNC to False in
        # settings.test, and there's unfortunately no better way to override
        # that here than by patching; see
        # https://github.com/django-es/django-elasticsearch-dsl/issues/322.
        with patch(
            "django_opensearch_dsl.apps.DODConfig.autosync_enabled",
            return_value=True,
        ):
            # Moving a page out of the parent should update the index so that
            # a search there now returns only 2 results.
            blog2.move(root)
            results = search.search(title="blog")
            self.assertEqual(len(results), 2)

            # Updating a page should also update the index so that a search
            # now returns only 1 result.
            blog3.title = "bar"
            blog3.save_revision().publish()
            results = search.search(title="blog")
            self.assertEqual(len(results), 1)

            # Deleting the remaining page with "blog" in the root should
            # result in an empty search result.
            blog1.delete()
            results = search.search(title="blog")
            self.assertFalse(results)
