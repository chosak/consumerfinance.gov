from django.test import TestCase

from foliage.contextmanagers import page_tree


class WagtailPageTreeTestCase(TestCase):
    """Mixin that creates a Wagtail page tree for tests.

    Test cases that inherit from this should define a get_page_tree()
    classmethod which returns the tree of pages to build.

    See https://pypi.org/project/wagtail-foliage/ for the page tree format.

    Sets a root_page property on the test case pointing to the first page in
    the tree.
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        pages = page_tree(cls.get_page_tree())
        pages.__enter__()
        cls.addClassCleanup(pages.__exit__, None, None, None)

        cls.root_page = pages.site.root_page

    @classmethod
    def get_page_tree(cls):
        raise NotImplementedError
