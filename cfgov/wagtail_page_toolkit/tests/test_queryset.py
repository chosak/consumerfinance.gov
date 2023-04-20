from django.test import TestCase

from wagtail.models import Page, Site
from wagtail.test.testapp.models import SimplePage

from wagtail_page_toolkit.queryset import get_page_for_url


class TestGetPageForURL(TestCase):
    def setUp(self):
        self.default_site = Site.objects.get(is_default_site=True)
        self.default_root_page = self.default_site.root_page.specific

        self.child_page = SimplePage(title="child", content="child", live=True)
        self.default_root_page.add_child(instance=self.child_page)

    def configure_default_site(self, hostname, port):
        self.default_site.hostname = hostname
        self.default_site.port = port
        self.default_site.save()

    def configure_second_site(self, hostname, port):
        self.second_root_page = SimplePage(
            title="second", content="second", live=True
        )
        wagtail_root = Page.objects.get(pk=1)
        wagtail_root.add_child(instance=self.second_root_page)

        self.second_site = Site.objects.create(
            hostname=hostname, port=port, root_page=self.second_root_page
        )

    def test_root_page_of_default_site_absolute_http_url(self):
        self.configure_default_site("example.com", 80)
        self.assertEqual(
            get_page_for_url("http://example.com/"), self.default_root_page
        )

    def test_root_page_of_default_site_absolute_https_url(self):
        self.configure_default_site("example.com", 443)
        self.assertEqual(
            get_page_for_url("https://example.com/"), self.default_root_page
        )

    def test_root_page_of_default_site_relative_url(self):
        self.configure_default_site("example.com", 80)
        self.assertEqual(get_page_for_url("/"), self.default_root_page)

    def test_child_page_of_default_site_absolute_url(self):
        self.configure_default_site("example.com", 443)
        self.assertEqual(
            get_page_for_url("https://example.com/child/"), self.child_page
        )

    def test_child_page_of_default_site_relative_url(self):
        self.configure_default_site("example.com", 443)
        self.assertEqual(get_page_for_url("/child/"), self.child_page)

    def test_invalid_absolute_url(self):
        self.configure_default_site("example.com", 443)
        self.assertIsNone(get_page_for_url("https://example.com/invalid/"))

    def test_invalid_relative_url(self):
        self.configure_default_site("example.com", 443)
        self.assertIsNone(get_page_for_url("/invalid/"))

    def test_different_hostname_single_site_returns_default_site(self):
        self.configure_default_site("example.com", 80)
        self.assertEqual(
            get_page_for_url("http://different.com/"), self.default_root_page
        )

    def test_root_page_of_second_site_absolute_url(self):
        self.configure_default_site("example.com", 80)
        self.configure_second_site("other.com", 80)
        self.assertEqual(
            get_page_for_url("http://other.com/"), self.second_root_page
        )

    def test_different_hostname_multiple_sites_returns_default_site(self):
        self.configure_default_site("example.com", 80)
        self.configure_second_site("other.com", 80)
        self.assertEqual(
            get_page_for_url("http://different.com/"), self.default_root_page
        )
