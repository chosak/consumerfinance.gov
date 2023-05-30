import json
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import date
from typing import List
from unittest import mock

from django.test import RequestFactory, SimpleTestCase, TestCase

from wagtail.models import Page, Site

from taggit.models import Tag

from core.testutils.test_cases import WagtailPageTreeTestCase
from v1.atomic_elements.organisms import FilterableList
from v1.models import AbstractFilterPage, BlogPage, BrowseFilterablePage
from v1.models.filterable_list_mixin import FilterableListMixin
from v1.util.ref import get_category_children


@dataclass
class MockSearchResults:
    min_start_date: date = field(default_factory=date.today)
    tag_slugs: List[str] = field(default_factory=list)
    language_codes: List[str] = field(default_factory=list)
    results: List[AbstractFilterPage] = field(default_factory=list)

    def __bool__(self):
        return bool(self.results)

    def __len__(self):
        return len(self.results)

    def __getitem__(self, key):
        return self.results[key]


class FilterableListMixinTests(WagtailPageTreeTestCase):
    @classmethod
    def get_page_tree(cls):
        return [
            BrowseFilterablePage(
                title="test-filterable-list",
                content=json.dumps(
                    [
                        {"type": "filter_controls", "value": {}},
                    ]
                ),
            ),
            [
                BlogPage(title="blog1"),
                BlogPage(title="blog2"),
            ],
        ]

    @contextmanager
    def mock_results(self, *results):
        with mock.patch(
            "v1.documents.FilterablePagesSearch.search", side_effect=results
        ):
            yield

    def test_nothing_to_filter(self):
        with self.mock_results(MockSearchResults()):
            response = self.client.get("/test-filterable-list/")

        # No results to filter, so don't show the form.
        self.assertIsNone(response.context_data["form"])
        self.assertFalse(response.context_data["has_unfiltered_results"])
        self.assertEqual(response.context_data["pages"].paginator.count, 0)

        # Filterable pages get a cache tag with the page's slug.
        self.assertEqual(response["Edge-Cache-Tag"], "test-filterable-list")

        # By default filterable pages are allowed to be indexed.
        self.assertIsNone(response.get("X-Robots-Tag"))

    def test_no_filters_applied(self):
        with self.mock_results(
            MockSearchResults(
                results=[
                    BlogPage.objects.get(slug="blog1"),
                    BlogPage.objects.get(slug="blog2"),
                ]
            )
        ):
            response = self.client.get("/test-filterable-list/")

        # Show the form with unfiltered results.
        self.assertTrue(response.context_data["form"])
        self.assertTrue(response.context_data["has_unfiltered_results"])
        self.assertEqual(response.context_data["pages"].paginator.count, 2)

        # By default filterable pages are allowed to be indexed.
        self.assertIsNone(response.get("X-Robots-Tag"))

    def test_no_results_after_filtering(self):
        with self.mock_results(
            MockSearchResults(
                results=[
                    BlogPage.objects.get(slug="blog1"),
                    BlogPage.objects.get(slug="blog2"),
                ]
            ),
            MockSearchResults(),
        ):
            response = self.client.get("/test-filterable-list/?title=test")

        # Show the form, no results, and an appropriate message.
        self.assertTrue(response.context_data["form"])
        self.assertTrue(response.context_data["has_unfiltered_results"])
        self.assertEqual(response.context_data["pages"].paginator.count, 0)
        self.assertContains(
            response,
            "Sorry, there were no results based on your filter selections.",
        )

        # For non-trivial searches, prevent indexing.
        self.assertEqual(response["X-Robots-Tag"], "noindex")

    def test_results_after_filtering(self):
        with self.mock_results(
            MockSearchResults(
                results=[
                    BlogPage.objects.get(slug="blog1"),
                    BlogPage.objects.get(slug="blog2"),
                ]
            ),
            MockSearchResults(
                results=[
                    BlogPage.objects.get(slug="blog1"),
                ]
            ),
        ):
            response = self.client.get("/test-filterable-list/?title=test")

        # Show the form and filtered results.
        self.assertTrue(response.context_data["form"])
        self.assertTrue(response.context_data["has_unfiltered_results"])
        self.assertEqual(response.context_data["pages"].paginator.count, 1)
        self.assertContains(response, "blog1")

        # For non-trivial searches, prevent indexing.
        self.assertEqual(response["X-Robots-Tag"], "noindex")

    def test_invalid_form_shows_no_results(self):
        with self.mock_results(
            MockSearchResults(
                results=[
                    BlogPage.objects.get(slug="blog1"),
                    BlogPage.objects.get(slug="blog2"),
                ]
            )
        ):
            response = self.client.get("/test-filterable-list/?topics=bad")

        # Show the form, no results, and an appropriate message.
        self.assertTrue(response.context_data["form"])
        self.assertTrue(response.context_data["has_unfiltered_results"])
        self.assertEqual(response.context_data["pages"].paginator.count, 0)
        self.assertContains(
            response,
            "Topics: Select a valid choice. bad is not one of the available choices.",
        )

        # Allow indexing of pages filtered by a single topic tag.
        self.assertIsNone(response.get("X-Robots-Tag"))

    def test_feed_view(self):
        response = self.client.get("/test-filterable-list/feed/")
        self.assertEqual(
            response["Content-Type"], "application/rss+xml; charset=utf-8"
        )
        self.assertEqual(response["Edge-Cache-Tag"], "test-filterable-list")
        self.assertEqual(response["Edge-Control"], "cache-maxage=10m")


class TestMixinGetFilterableSearch(TestCase):
    def test_no_filterable_list_block_defaults(self):
        page = BrowseFilterablePage(title="test")

        search = page.get_filterable_search()
        self.assertEqual(search.root_page, page)
        self.assertEqual(search.children_only, True)
        self.assertEqual(search.ordering, FilterableList.DEFAULT_ORDERING)

    def test_search_default_children_only(self):
        page = BrowseFilterablePage(
            title="test",
            content=json.dumps(
                [
                    {"type": "filter_controls", "value": {}},
                ]
            ),
        )

        search = page.get_filterable_search()
        self.assertEqual(search.root_page, page)
        self.assertEqual(search.children_only, True)
        self.assertEqual(search.ordering, FilterableList.DEFAULT_ORDERING)

    def test_search_children_only_true(self):
        page = BrowseFilterablePage(
            title="test",
            content=json.dumps(
                [
                    {
                        "type": "filter_controls",
                        "value": {
                            "filter_children": True,
                        },
                    },
                ]
            ),
        )

        search = page.get_filterable_search()
        self.assertEqual(search.root_page, page)
        self.assertEqual(search.children_only, True)
        self.assertEqual(search.ordering, FilterableList.DEFAULT_ORDERING)

    def test_search_children_only_false_uses_default_site_if_not_in_site(self):
        page = BrowseFilterablePage(
            title="test",
            content=json.dumps(
                [
                    {
                        "type": "filter_controls",
                        "value": {
                            "filter_children": False,
                        },
                    },
                ]
            ),
        )

        search = page.get_filterable_search()
        self.assertEqual(
            search.root_page,
            Site.objects.get(is_default_site=True).root_page,
        )
        self.assertEqual(search.children_only, False)
        self.assertEqual(search.ordering, FilterableList.DEFAULT_ORDERING)

    def test_search_children_only_false_uses_site_root(self):
        page = BrowseFilterablePage(
            title="test",
            content=json.dumps(
                [
                    {
                        "type": "filter_controls",
                        "value": {
                            "filter_children": False,
                        },
                    },
                ]
            ),
        )

        Page.objects.get(pk=1).add_child(instance=page)
        Site.objects.create(root_page=page)

        search = page.get_filterable_search()
        self.assertEqual(search.root_page.specific, page)
        self.assertEqual(search.children_only, False)
        self.assertEqual(search.ordering, FilterableList.DEFAULT_ORDERING)

    def test_search_different_ordering(self):
        page = BrowseFilterablePage(
            title="test",
            content=json.dumps(
                [
                    {
                        "type": "filter_controls",
                        "value": {
                            "ordering": "title.raw",
                        },
                    },
                ]
            ),
        )

        search = page.get_filterable_search()
        self.assertEqual(search.root_page, page)
        self.assertEqual(search.children_only, True)
        self.assertEqual(search.ordering, "title.raw")


class TestMixinGetForm(TestCase):
    def setUp(self):
        Tag.objects.create(name="Foo", slug="foo")
        Tag.objects.create(name="Bar", slug="bar")

        self.results = MockSearchResults(
            tag_slugs=["foo", "bar"],
            language_codes=["en", "es"],
        )
        self.data = {"some": "thing"}

    def test_get_form_default(self):
        class MockPage(FilterableListMixin):
            pass

        form = MockPage().get_form(self.results, self.data)
        self.assertEqual(form.initial, {})
        self.assertEqual(form.data, self.data)
        self.assertEqual(form.default_min_date, self.results.min_start_date)
        self.assertEqual(
            form.fields["topics"].choices,
            [("bar", "Bar"), ("foo", "Foo")],
        )
        self.assertEqual(
            form.fields["language"].choices,
            [("en", "English"), ("es", "Spanish")],
        )

    def test_get_form_customized(self):
        class MockPage(FilterableListMixin):
            filterable_categories = ["Blog", "Newsroom"]
            filterable_page_type = BrowseFilterablePage

        form = MockPage().get_form(self.results, self.data)
        self.assertEqual(
            form.initial,
            {
                "categories": get_category_children(
                    MockPage.filterable_categories
                ),
                "model_class": BrowseFilterablePage.__name__,
            },
        )
        self.assertEqual(form.data, self.data)
        self.assertEqual(form.default_min_date, self.results.min_start_date)
        self.assertEqual(
            form.fields["topics"].choices,
            [("bar", "Bar"), ("foo", "Foo")],
        )
        self.assertEqual(
            form.fields["language"].choices,
            [("en", "English"), ("es", "Spanish")],
        )


class TestMixinPaginateResults(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_pagination_default(self):
        class MockPage(FilterableListMixin):
            pass

        request = self.factory.get("/")
        results_page = MockPage().paginate_results(request, list(range(100)))
        self.assertEqual(results_page.object_list, list(range(25)))
        request = self.factory.get("/?page=2")
        results_page = MockPage().paginate_results(request, list(range(100)))
        self.assertEqual(results_page.object_list, list(range(25, 50)))

        request = self.factory.get("/?page=bad")
        results_page = MockPage().paginate_results(request, list(range(100)))
        self.assertEqual(results_page.object_list, list(range(25)))

        request = self.factory.get("/?page=")
        results_page = MockPage().paginate_results(request, list(range(100)))
        self.assertEqual(results_page.object_list, list(range(25)))

        request = self.factory.get("/?page=10000")
        results_page = MockPage().paginate_results(request, list(range(100)))
        self.assertEqual(results_page.object_list, list(range(75, 100)))

    def test_pagination_custom(self):
        class MockPage(FilterableListMixin):
            filterable_per_page_limit = 30

        request = self.factory.get("/")
        results_page = MockPage().paginate_results(request, list(range(100)))
        self.assertEqual(results_page.object_list, list(range(30)))

        request = self.factory.get("/?page=2")
        results_page = MockPage().paginate_results(request, list(range(100)))
        self.assertEqual(results_page.object_list, list(range(30, 60)))
