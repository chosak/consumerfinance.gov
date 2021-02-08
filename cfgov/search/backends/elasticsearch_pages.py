import sys

from django.db.models.lookups import Lookup

from wagtail.core.models import Page
from wagtail.search import index
from wagtail.search.backends.base import FilterFieldError

from search.index import RelatedFilterField


# Elasticsearch 7 may be installed as 'elasticsearch7', but Wagtail's ES code
# assume that it is installed as 'elasticsearch'. Temporarily patch the import
# so that ES7 is imported from 'elasticsearch'.
elasticsearch = __import__('elasticsearch')
if elasticsearch.VERSION < (7,):
    sys.modules['elasticsearch'] = __import__('elasticsearch7')

 
from wagtail.search.backends.elasticsearch7 import (  # noqa: E402
    Elasticsearch7SearchBackend, Elasticsearch7SearchQueryCompiler
)


sys.modules['elasticsearch'] = elasticsearch


# https://docs.wagtail.io/en/v2.12/topics/search/indexing.html#index-relatedfields
class PageSearchQueryCompiler(Elasticsearch7SearchQueryCompiler):
    def NOT_get_filterable_field(self, field_attname):
        field = super()._get_filterable_field(field_attname)

        if field:
            return field

        # We may be looking for a related field.
        related_fields = [
            field for field in self.queryset.model.get_search_fields()
            if isinstance(field, RelatedFilterField)
        ]

        for related_field in related_fields:
            if field_attname == '__'.join([
                related_field.field_name,
                related_field.related_field_name
            ]):
                return related_field

        return None

    def _get_filters_from_where_node(self, where_node, check_only=False):
        try:
            return super()._get_filters_from_where_node(
                where_node,
                check_only=check_only
            )
        except FilterFieldError:
            if isinstance(where_node, Lookup):
                # This might be a FilterField defined within a RelatedFields.
                # If so, we need to create a nested filter here.
                field_attname = where_node.lhs.target.attname

                join = self.queryset.query.alias_map[where_node.lhs.alias]
                join_field_name = join.join_field.name
                field_attname = join_field_name + '__' + field_attname

                lookup = where_node.lookup_name
                value = where_node.rhs

                return self._process_filter(
                    field_attname,
                    lookup,
                    value,
                    check_only=check_only
                )

            # We were unable to find an appropriate filter to use, so raise the
            # original exception from above.
            raise

            if False:
                #
                # A rough way of determining this is by checking the lookup to see
                # if it is a join to some other model that isn't part of the Page
                # hierarchy. This wont work in all cases, for example if a page
                # legitimately has a foreign key to some other page model. Buu
                # this should be good enough for most other cases.
                if not issubclass(
                    self.queryset.model,
                    where_node.lhs.target.model
                ):
                    # Normally the field_attname will be the name of the field on
                    # the model that was indexed. In this case, we instead need
                    # to preface it with the name of the related model.
                    import pdb; pdb.set_trace()
                    field_attname = where_node.lhs.target.attname

                    join = self.queryset.query.alias_map[where_node.lhs.alias]
                    join_field_name = join.join_field.name
                    field_attname = join_field_name + '__' + field_attname

                    lookup = where_node.lookup_name
                    value = where_node.rhs

                    return self._process_filter(
                        field_attname,
                        lookup,
                        value,
                        check_only=check_only
                    )

            return super()._get_filters_from_where_node(
                where_node,
                check_only=check_only
            )


class PageSearchBackend(Elasticsearch7SearchBackend):
    query_compiler_class = PageSearchQueryCompiler

    def get_index_for_model(self, model):
        if issubclass(model, Page):
            return super().get_index_for_model(model)


SearchBackend = PageSearchBackend
