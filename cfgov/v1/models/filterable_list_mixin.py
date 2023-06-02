from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.contrib.routable_page.models import route
from wagtail.models import Site
from wagtailsharing.models import ShareableRoutablePageMixin

from v1.atomic_elements.organisms import FilterableList
from v1.documents import FilterablePagesSearch
from v1.feeds import FilterableFeed
from v1.util.ref import get_category_children


class FilterableListMixin(ShareableRoutablePageMixin):
    """Wagtail Page mixin that allows for filtering of other pages."""

    filterable_per_page_limit = 25
    """Number of results to return per page."""

    filterable_categories = []
    """Determines default page category filtering."""

    filterable_page_type = None
    """Allow limiting results to a specific page type."""

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        form = None
        pages = None

        # We always do an unfiltered search to determine the list of
        # possible topics and languages to display in the form, as well as
        # the default from_date to use if only to_date is provided.
        # This search also tells us if there are any results to be filtered.
        search = self.get_filterable_search()
        unfiltered_results = search.search(include_aggregates=True)

        # By default we show unfiltered results unless they are being filtered.
        results = self.paginate_results(request, unfiltered_results)

        # If there is data to be filtered, create a form to filter it.
        if results:
            form = self.get_form(results.object_list, request.GET)

            # If any filters are applied, we might need to do another search.
            if form.has_active_filters:
                if form.is_valid():
                    filtered_results = search.search(**form.cleaned_data)
                else:
                    # If the form was invalid, we don't show any results.
                    filtered_results = []

                results = self.paginate_results(request, filtered_results)

        context.update(
            {
                "form": form,
                "has_unfiltered_results": bool(unfiltered_results),
                "pages": results,
            }
        )

        return context

    def get_filterable_search(self):
        # Look for a FilterableList block in the content field.
        block = self.content.first_block_by_name("filter_controls")
        value = block.value if block else {}

        # By default, filterable pages only search their direct children.
        # But this can be overriden by a setting on a FilterableList block
        # added to the page's content StreamField.
        children_only = value.get("filter_children", True)

        # Default filterable list ordering can also be overridden.
        ordering = value.get("ordering", FilterableList.DEFAULT_ORDERING)

        # If searching globally, use the root page of this page's Wagtail
        # Site. If the page doesn't live under a Site (for example, it is
        # in the Trash), use the default Site.
        if not children_only:
            site = self.get_site()

            if not site:
                site = Site.objects.get(is_default_site=True)

            search_root = site.root_page
        else:
            search_root = self

        return FilterablePagesSearch(
            search_root, children_only=children_only, ordering=ordering
        )

    def get_form(self, unfiltered_results, form_data):
        from v1.forms import FilterableListForm

        initial_data = {}

        if self.filterable_categories:
            initial_data["categories"] = get_category_children(
                self.filterable_categories
            )

        if self.filterable_page_type:
            initial_data["model_class"] = self.filterable_page_type.__name__

        return FilterableListForm(
            initial=initial_data,
            data=form_data,
            default_min_date=unfiltered_results.min_start_date,
            topic_slugs=unfiltered_results.tag_slugs,
            language_codes=unfiltered_results.language_codes,
        )

    def paginate_results(self, request, results):
        paginator = Paginator(results, self.filterable_per_page_limit)
        page = request.GET.get("page")

        try:
            results_page = paginator.page(page)
        except PageNotAnInteger:
            results_page = paginator.page(1)
        except EmptyPage:
            results_page = paginator.page(paginator.num_pages)

        return results_page

    def render(self, request, *args, **kwargs):
        """Render with optional X-Robots-Tag in response headers"""
        response = super().render(request, *args, **kwargs)

        # Set noindex for crawlers if we did complex filtering.
        form = response.context_data.get("form")
        if form and form.do_not_index:
            response["X-Robots-Tag"] = "noindex"

        return response

    def serve(self, request, *args, **kwargs):
        # Set a cache key for this filterable list page.
        # We do this in `serve()` so that it gets applied to all routes, not
        # just routes that use `render()`.
        response = super().serve(request, *args, **kwargs)
        response["Edge-Cache-Tag"] = self.slug
        return response

    @route(r"^$")
    def index_route(self, request):
        return self.render(request)

    @route(r"^feed/$")
    def feed_route(self, request, *args, **kwargs):
        context = self.get_context(request)
        return FilterableFeed(self, context)(request)
