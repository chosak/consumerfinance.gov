from django import forms
from django.utils.functional import cached_property

from wagtail.contrib.table_block.blocks import (
    TableBlock,
    TableInput,
    TableInputAdapter,
)
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.core import blocks
from wagtail.core.telepath import register

from v1.blocks import HeadingBlock


class RichTextTableInput(TableInput):
    @cached_property
    def media(self):
        media = super().media
        rich_text_media = forms.Media(
            js=["apps/admin/js/rich-text-table.js"],
        )
        return media + rich_text_media


class RichTextTableInputAdapter(TableInputAdapter):
    js_constructor = "v1.widgets.RichTextTableInput"


register(RichTextTableInputAdapter(), RichTextTableInput)


class AtomicTableBlock(TableBlock):
    label = "Table (deprecated)"
    table_options = {"renderer": "html"}

    @cached_property
    def field(self):
        widget = RichTextTableInput(table_options=self.table_options)
        return forms.CharField(widget=widget, **self.field_options)

    def to_python(self, value):
        new_value = super().to_python(value)
        if new_value:
            new_value["has_data"] = self.get_has_data(new_value)
        return new_value

    def get_has_data(self, value):
        has_data = False
        if value and "data" in value:
            first_row_index = (
                1 if value.get("first_row_is_table_header", None) else 0
            )
            first_col_index = (
                1 if value.get("first_col_is_header", None) else 0
            )

            for row in value["data"][first_row_index:]:
                for cell in row[first_col_index:]:
                    if cell:
                        has_data = True
                        break
                if has_data:
                    break
        return has_data

    def get_table_options(self, table_options=None):
        collected_table_options = super().get_table_options(
            table_options=table_options
        )
        collected_table_options["editor"] = "RichTextEditor"
        collected_table_options["outsideClickDeselects"] = False
        return collected_table_options

    class Meta:
        default = None
        icon = "table"
        template = "v1/includes/organisms/table.html"
        label = "Table (deprecated)"


class TableBlock(blocks.StructBlock):
    heading = HeadingBlock()
    column_width = blocks.ChoiceBlock(
        choices=(
            (c, c)
            for c in (
                ["Automatic"]
                + [f"{percent}%" for percent in range(10, 100, 10)]
            )
        ),
        default="Flexible width",
    )
    options = blocks.MultipleChoiceBlock(
        choices=[
            ("first_column_is_header", "Display the first column as a header"),
            ("first_row_is_header", "Display the first row as a header"),
            ("is_full_width", "Display the table at full width"),
            ("is_striped", "Display the table with striped rows"),
            ("is_stacked", "Stack the table columns on mobile"),
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    data = TypedTableBlock(
        [
            ("text", blocks.CharBlock()),
            ("numeric", blocks.FloatBlock()),
            (
                "rich_text",
                blocks.RichTextBlock(
                    features=[
                        "bold",
                        "italic",
                        "h3",
                        "h4",
                        "h5",
                        "ol",
                        "ul",
                        "link",
                        "document-link",
                    ]
                ),
            ),
        ]
    )

    class Meta:
        icon = "table"
        label = "Table"
        template = "v1/includes/organisms/table2.html"
