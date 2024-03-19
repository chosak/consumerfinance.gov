# -*- coding: utf-8 -*-
from django.test import TestCase

from wagtail.models import Site

from v1.blocks import ReusableTextChooserBlock
from v1.models import (
    Contact,
    EmailSignUp,
    ReusableNotification,
    ReusableText,
    SublandingPage,
)


class TestUnicodeCompatibility(TestCase):
    def test_unicode_contact_heading_unicode(self):
        contact = Contact(heading="Unicod\xeb")
        self.assertEqual(str(contact), "Unicod\xeb")
        self.assertIsInstance(str(contact), str)


class TestModelStrings(TestCase):
    def test_reusable_text_string(self):
        test_snippet = ReusableText(
            title="Snippet title",
            sidefoot_heading="Sidefoot heading",
            text="Snippet text",
        )
        self.assertEqual(str(test_snippet), test_snippet.title)

    def test_email_signup_string(self):
        test_snippet = EmailSignUp(
            topic="Test signup",
            url="http://test/signup",
            code="TEST_CODE",
        )
        self.assertEqual(str(test_snippet), "Test signup (http://test/signup)")

        test_snippet = EmailSignUp(
            topic="Test signup",
            code="TEST_CODE",
        )
        self.assertEqual(str(test_snippet), "Test signup (TEST_CODE)")


class TestReusableTextRendering(TestCase):
    def test_links_get_expanded(self):
        page = SublandingPage(title="foo", slug="foo")
        default_site = Site.objects.get(is_default_site=True)
        default_site.root_page.add_child(instance=page)

        html = '<a linktype="page" id="{}">Link</a>'.format(page.pk)
        block = ReusableTextChooserBlock(ReusableText)
        self.assertIn('<a href="/foo/">', block.render({"text": html}))

    def test_nonexistent_links_return_empty_link(self):
        html = '<a linktype="page" id="12345">Link</a>'
        block = ReusableTextChooserBlock(ReusableText)
        self.assertIn("<a>", block.render({"text": html}))


class ReusableNotificationTestCase(TestCase):
    def test_title_str(self):
        notification = ReusableNotification(title="Warning Notification")
        self.assertEqual(str(notification), "Warning Notification")
