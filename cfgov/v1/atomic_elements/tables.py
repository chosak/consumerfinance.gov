from django import forms

from wagtail import blocks
from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail.documents.blocks import DocumentChooserBlock

from v1.blocks import HeadingBlock


class ContactUsRow(blocks.StructBlock):
    title = blocks.CharBlock()
    body = blocks.RichTextBlock(features=["bold", "italic", "link"])


class ContactUsTable(blocks.StructBlock):
    heading = blocks.CharBlock()
    rows = blocks.ListBlock(ContactUsRow, collapsed=True, min_num=1)

    class Meta:
        icon = "table"
        template = "v1/includes/organisms/tables/contact-us.html"
        label = "Table (Contact Us)"
        unescape = False


class ConsumerReportingCompanyTable(blocks.StructBlock):
    website = blocks.RichTextBlock(features=["bold", "italic", "link"])
    phone = blocks.RichTextBlock(features=["bold", "italic", "link"])
    mailing_address = blocks.RichTextBlock(features=["bold", "italic", "link"])

    class Meta:
        icon = "table"
        template = (
            "v1/includes/organisms/tables/consumer-reporting-company.html"
        )
        label = "Table (Consumer Reporting Company)"


class CaseDocketEventAttachment(blocks.StructBlock):
    id = blocks.CharBlock()
    title = blocks.CharBlock()
    document = DocumentChooserBlock(required=False)


class CaseDocketEvent(blocks.StructBlock):
    index = blocks.CharBlock()
    date_filed = blocks.DateBlock()
    document = DocumentChooserBlock(required=False)
    description = blocks.CharBlock()
    filed_by = blocks.CharBlock()
    attachments = blocks.ListBlock(
        CaseDocketEventAttachment, collapsed=True, default=[]
    )

    class Meta:
        label_format = "{index} - {description}"


class CaseDocketTable(blocks.StructBlock):
    events = blocks.ListBlock(CaseDocketEvent, collapsed=True, min_num=1)

    class Meta:
        icon = "table"
        template = "v1/includes/organisms/tables/case-docket.html"
        label = "Table (Case Docket)"
        unescape = False


class Table(blocks.StructBlock):
    heading = HeadingBlock(required=False)
    options = blocks.MultipleChoiceBlock(
        choices=[
            ("is_full_width", "Display the table at full width"),
            ("stack_on_mobile", "Stack the table columns on mobile"),
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
                        "ol",
                        "ul",
                        "link",
                        "document-link",
                        "superscript",
                    ]
                ),
            ),
        ]
    )

    class Meta:
        icon = "table"
        template = "v1/includes/organisms/tables/base.html"
        unescape = False
