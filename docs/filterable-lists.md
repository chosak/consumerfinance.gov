# Filterable Lists

[As described in the CFPB Design System](https://cfpb.github.io/design-system/pages/filterable-list-pages),
filterable list pages house searchable lists of articles, documents, or other resources or publications.
Several Wagtail page types in this project implement this pattern to provide a broad,
configurable search and filtering interface across multiple areas of our site.

- [Overview](#overview)
- [Indexing and search](#indexing-and-search)
- [`FilterableListMixin`](#filterablelistmixin)
- [`FilterableList`](#filterablelist)

## Overview

Creating a page with a filterable list requires two things:

- the page type must inherit from the
  [`FilterableListMixin`](https://github.com/cfpb/consumerfinance.gov/blob/7b9084eb6747f002fc4c1a976590c3366d9845ff/cfgov/v1/models/filterable_list_mixins.py#L14) mixin.
- the page must be configured with a special
  [`FilterableList`](https://github.com/cfpb/consumerfinance.gov/blob/7b9084eb6747f002fc4c1a976590c3366d9845ff/cfgov/v1/atomic_elements/organisms.py#L684)
  StreamField block.

When these two requirements are met, the page will support displaying a list of other pages on the site.

By default, a page displays a paginated list of its direct children that inherit from the
[`AbstractFilterPage`](https://github.com/cfpb/consumerfinance.gov/blob/7b9084eb6747f002fc4c1a976590c3366d9845ff/cfgov/v1/models/learn_page.py#L31) page type.
The exact style and functionality of both the user-facing filter controls and the list of search results can be customized, either via editor controls on the `FilterableList` block or via the source code of `FilterableListMixin` page types.

Under the hood, search is powered by an
[OpenSearch](https://opensearch.org/)
search index that mirrors the content of `AbstractFilterPage` pages
on the website. Filterable lists allow for text-based content search and filtering by date range, page topics and categories, and more.

## Indexing and search

Wagtail pages are indexed into OpenSearch using the
[django-opensearch-dsl](https://django-opensearch-dsl.readthedocs.io/en/latest/)
package.

The
[`FilterablePageDocument`](https://github.com/cfpb/consumerfinance.gov/blob/5d7483cc4d8a20d121590e5a89e8fef5569d2c93/cfgov/v1/documents.py#L23)
class implements a django-opensearch-dsl
[document](https://django-opensearch-dsl.readthedocs.io/en/latest/document/) that is used to index data related to any of the filterable page types that extend `AbstractFilterPage`, including `BlogPage`, `EnforcementActionPage`, `EventPage`, and `NewsroomPage`.

The django-opensearch-dsl
[Django management commands](https://django-opensearch-dsl.readthedocs.io/en/latest/management/)
`manage.py opensearch index` and `manage.py opensearch document` are used to create and populate an OpenSearch index with filterable page data.
The index is also automatically kept up to date with changes when pages are published or moved.

The
[`FilterablePagesSearch`](https://github.com/cfpb/consumerfinance.gov/blob/5d7483cc4d8a20d121590e5a89e8fef5569d2c93/cfgov/v1/documents.py#L114)
class is used to make queries against the search index.

## `FilterableListMixin`

The
[`FilterableMixin`](https://github.com/cfpb/consumerfinance.gov/blob/7b9084eb6747f002fc4c1a976590c3366d9845ff/cfgov/v1/models/filterable_list_mixins.py#L14)
mixin adds filtering capability to Wagtail page types that inherit from it.
The bulk of the mixin's work is done in its `get_context` method, which searches the index to retrieve results appropriate to the user's request.
Those results are then rendered as part of the page.

The mixin defines various attributes which can be overriden to customize its functionality:

### `filterable_per_page_limit`

Number of results to show per page. Defaults to 25.

### `filterable_categories`

When defined as a list of page categories, only pages from those categories will be included in filter results.
Defaults to an empty list.

For example, the `NewsroomLandingPage` page type sets this attribute this way:

```py
class NewsroomLandingPage:
    filterable_categories = ["Blog", "Newsroom"]
```

so that only pages from these categories appear in filter results.

### `filterable_page_type`

When set to a Wagtail page type, only pages of that type will be included in filter results.
Defaults to `None`, meaning that any available pages in the search space may be returned.

For example, the `EventArchivePage` page types sets this attribute this way:

```py
class EventArchivePage:
    filterable_page_type = EventPage
```

so that only pages of that type appear in filter results.

## `FilterableList`

[`FilterableList`](<(https://github.com/cfpb/consumerfinance.gov/blob/7b9084eb6747f002fc4c1a976590c3366d9845ff/cfgov/v1/atomic_elements/organisms.py#L684)>)
is the StreamField block that must be added to a page to render search results. This block contains numerous configuration options that determine how results are filtered and what filtering choices are displayed to the end user.
