from operator import attrgetter
from urllib.parse import urlparse

from django.db.models import Q
from django.http import Http404, HttpRequest

from wagtail.models import Page, Site


def get_page_for_url(url):
    parsed_url = urlparse(url)
    request = HttpRequest()

    if not parsed_url.hostname:
        site = Site.objects.get(is_default_site=True)
        request.META = {"HTTP_HOST": site.hostname, "SERVER_PORT": site.port}
    else:
        request.META = {
            "HTTP_HOST": parsed_url.hostname,
            "SERVER_PORT": parsed_url.port
            or (443 if parsed_url.scheme == "https" else 80),
        }
        site = Site.find_for_request(request)

    path_components = [c for c in parsed_url.path.split("/") if c]

    try:
        page, args, kwargs = site.root_page.localized.specific.route(
            request, path_components
        )
    except Http404:
        return None

    return page


def build_page_queryset(
    page_ids=None,
    page_urls=None,
    page_types=None,
    include_descendants=False,
    include_descendants_only=False,
):
    if page_ids or page_urls:
        all_page_ids = list(page_ids or [])

    if page_urls:
        url_pages = list(map(get_page_for_url, page_urls))

        bad_urls = [url for url, page in zip(page_urls, url_pages) if not page]
        if bad_urls:
            raise ValueError(
                f"Could not find page for URL(s): {', '.join(bad_urls)}"
            )

        all_page_ids.extend(map(attrgetter("id"), url_pages))

    if page_types:
        qs = qs.type(*page_types)

        parser.add_argument(
            "--page-id",
            type=wagtail_page_id_type,
            nargs="*",
            dest="page_id",
            help="Page ID",
        )
        parser.add_argument(
            "--url",
        )
        parser.add_argument(
            "--urlfile",
        )
        parser.add_argument(
            "--page-type",
            type=wagtail_page_type_type,
            nargs="*",
            dest="page_types",
            help="Wagtail page type, specified as 'appname.modelname'",
        )
        parser.add_argument(
            "--include-descendants",
            action="store_true",
            help="Include page descendants",
        )
        parser.add_argument(
            "--include-descendants-only",
            action="store_true",
            help="Include only page descendants",
        )
