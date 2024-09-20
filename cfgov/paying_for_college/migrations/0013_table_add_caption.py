# Generated by Django 4.2.16 on 2024-09-20 17:26

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('paying_for_college', '0012_add_footnotes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegecostspage',
            name='content',
            field=wagtail.fields.StreamField([('full_width_text', 41), ('info_unit_group', 52), ('expandable_group', 60), ('expandable', 58), ('well', 40), ('raw_html_block', 61)], blank=True, block_lookup={0: ('wagtail.blocks.RichTextBlock', (), {'icon': 'edit'}), 1: ('wagtail.blocks.RichTextBlock', (), {}), 2: ('wagtail.blocks.CharBlock', (), {'help_text': '\n            ID will be auto-generated on save.\n            However, you may enter some human-friendly text that\n            will be incorporated to make it easier to read.\n        ', 'label': 'ID for this content block', 'required': False}), 3: ('wagtail.blocks.StructBlock', [[('link_id', 2)]], {}), 4: ('wagtail.blocks.StructBlock', [[('content_block', 1), ('anchor_link', 3)]], {}), 5: ('wagtail_footnotes.blocks.RichTextBlockWithFootnotes', (), {'features': ['anchor-identifier', 'h2', 'h3', 'h4', 'h5', 'hr', 'ol', 'ul', 'bold', 'italic', 'superscript', 'blockquote', 'link', 'document-link', 'image', 'icon', 'footnotes']}), 6: ('wagtail.blocks.CharBlock', (), {'required': False}), 7: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5')]}), 8: ('wagtail.blocks.CharBlock', (), {'help_text': 'Input the name of an icon to appear to the left of the heading. E.g., approved, help-round, etc. <a href="https://cfpb.github.io/design-system/foundation/iconography">See full list of icons</a>', 'required': False}), 9: ('wagtail.blocks.StructBlock', [[('text', 6), ('level', 7), ('icon', 8)]], {'required': False}), 10: ('wagtail.images.blocks.ImageChooserBlock', (), {'required': False}), 11: ('wagtail.blocks.CharBlock', (), {'help_text': "No character limit, but be as succinct as possible. If the image is decorative (i.e., a screenreader wouldn't have anything useful to say about it), leave this field blank.", 'required': False}), 12: ('wagtail.blocks.StructBlock', [[('upload', 10), ('alt', 11)]], {}), 13: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('full', 'Full width'), (470, '470px'), (270, '270px'), (170, '170px')]}), 14: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('right', 'right'), ('left', 'left')], 'help_text': 'Does not apply if the image is full-width'}), 15: ('wagtail.blocks.RichTextBlock', (), {'label': 'Caption', 'required': False}), 16: ('wagtail.blocks.BooleanBlock', (), {'default': True, 'help_text': 'Check to add a horizontal rule line to bottom of inset.', 'label': 'Has bottom rule line', 'required': False}), 17: ('wagtail.blocks.StructBlock', [[('image', 12), ('image_width', 13), ('image_position', 14), ('text', 15), ('is_bottom_rule', 16)]], {}), 18: ('wagtail.blocks.MultipleChoiceBlock', [], {'choices': [('is_full_width', 'Display the table at full width'), ('stack_on_mobile', 'Stack the table columns on mobile')], 'required': False}), 19: ('wagtail.blocks.CharBlock', (), {}), 20: ('wagtail.blocks.FloatBlock', (), {}), 21: ('wagtail.blocks.RichTextBlock', (), {'features': ['bold', 'italic', 'ol', 'ul', 'link', 'document-link', 'superscript']}), 22: ('wagtail_footnotes.blocks.RichTextBlockWithFootnotes', (), {'features': ['bold', 'italic', 'ol', 'ul', 'link', 'document-link', 'superscript', 'footnotes']}), 23: ('wagtail.contrib.typed_table_block.blocks.TypedTableBlock', [[('text', 19), ('numeric', 20), ('rich_text', 21), ('rich_text_with_footnotes', 22)]], {}), 24: ('wagtail.blocks.RichTextBlock', (), {'required': False}), 25: ('wagtail.blocks.StructBlock', [[('heading', 9), ('text_introduction', 6), ('options', 18), ('data', 23), ('caption', 24)]], {}), 26: ('wagtail.blocks.TextBlock', (), {}), 27: ('wagtail.blocks.TextBlock', (), {'required': False}), 28: ('wagtail.blocks.StructBlock', [[('body', 26), ('citation', 27)]], {}), 29: ('wagtail.blocks.CharBlock', (), {'help_text': 'Add an ARIA label if the link text does not describe the destination of the link (e.g. has ambiguous text like "Learn more" that is not descriptive on its own).', 'required': False}), 30: ('wagtail.blocks.CharBlock', (), {'default': '/', 'required': False}), 31: ('wagtail.blocks.BooleanBlock', (), {'default': False, 'required': False}), 32: ('wagtail.blocks.StructBlock', [[('text', 6), ('aria_label', 29), ('url', 30), ('is_link_boldface', 31)]], {}), 33: ('wagtail.blocks.StructBlock', [[('slug_text', 6), ('paragraph_text', 24), ('button', 32)]], {}), 34: ('wagtail.blocks.ListBlock', (32,), {}), 35: ('wagtail.blocks.StructBlock', [[('heading', 6), ('paragraph', 24), ('links', 34)]], {}), 36: ('v1.blocks.ReusableTextChooserBlock', ('v1.ReusableText',), {}), 37: ('v1.blocks.ReusableNotificationChooserBlock', ('v1.ReusableNotification',), {}), 38: ('v1.blocks.EmailSignUpChooserBlock', (), {}), 39: ('wagtail.blocks.RichTextBlock', (), {'label': 'Well', 'required': False}), 40: ('wagtail.blocks.StructBlock', [[('content', 39)]], {}), 41: ('wagtail.blocks.StreamBlock', [[('content', 0), ('content_with_anchor', 4), ('content_with_footnotes', 5), ('heading', 9), ('image', 17), ('table', 25), ('quote', 28), ('cta', 33), ('related_links', 35), ('reusable_text', 36), ('reusable_notification', 37), ('email_signup', 38), ('well', 40)]], {}), 42: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('50-50', '50/50'), ('33-33-33', '33/33/33'), ('25-75', '25/75')], 'help_text': 'Choose the number and width of info unit columns.', 'label': 'Format'}), 43: ('wagtail.blocks.BooleanBlock', (), {'default': True, 'help_text': "Check this to link all images and headings to the URL of the first link in their unit's list, if there is a link.", 'required': False}), 44: ('wagtail.blocks.BooleanBlock', (), {'default': False, 'help_text': 'Check this to add a horizontal rule line to top of info unit group.', 'required': False}), 45: ('wagtail.blocks.BooleanBlock', (), {'default': False, 'help_text': 'Check this to show horizontal rule lines between info units.', 'label': 'Show rule lines between items', 'required': False}), 46: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('none', 'None'), ('rounded', 'Rounded corners'), ('circle', 'Circle')], 'help_text': 'Adds a <em>border-radius</em> class to images in this group, allowing for a rounded or circular border.', 'label': 'Border radius for images?', 'required': False}), 47: ('wagtail.blocks.StructBlock', [[('text', 6), ('level', 7), ('icon', 8)]], {'default': {'level': 'h3'}, 'required': False}), 48: ('wagtail.blocks.RichTextBlock', (), {'blank': True, 'required': False}), 49: ('wagtail.blocks.ListBlock', (32,), {'required': False}), 50: ('wagtail.blocks.StructBlock', [[('image', 12), ('heading', 47), ('body', 48), ('links', 49)]], {}), 51: ('wagtail.blocks.ListBlock', (50,), {'default': []}), 52: ('wagtail.blocks.StructBlock', [[('format', 42), ('heading', 9), ('intro', 24), ('link_image_and_heading', 43), ('has_top_rule_line', 44), ('lines_between_items', 45), ('border_radius_image', 46), ('info_units', 51)]], {}), 53: ('wagtail.blocks.CharBlock', (), {'help_text': 'Added as an <code>&lt;h3&gt;</code> at the top of this block. Also adds a wrapping <code>&lt;div&gt;</code> whose <code>id</code> attribute comes from a slugified version of this heading, creating an anchor that can be used when linking to this part of the page.', 'required': False}), 54: ('wagtail.blocks.BooleanBlock', (), {'required': False}), 55: ('wagtail.blocks.BooleanBlock', (), {'default': False, 'help_text': 'Check this to add a horizontal rule line to top of expandable group.', 'required': False}), 56: ('wagtail.blocks.BooleanBlock', (), {'default': False, 'help_text': 'Check this to add FAQ schema markup to expandables.', 'label': 'Uses FAQ schema', 'required': False}), 57: ('wagtail.blocks.StreamBlock', [[('paragraph', 24), ('well', 40), ('links', 32), ('info_unit_group', 52)]], {'blank': True}), 58: ('wagtail.blocks.StructBlock', [[('label', 6), ('icon', 6), ('is_bordered', 54), ('is_midtone', 54), ('is_expanded', 54), ('is_expanded_padding', 54), ('content', 57)]], {}), 59: ('wagtail.blocks.ListBlock', (58,), {}), 60: ('wagtail.blocks.StructBlock', [[('heading', 53), ('body', 24), ('is_accordion', 54), ('has_top_rule_line', 55), ('is_faq', 56), ('expandables', 59)]], {}), 61: ('wagtail.blocks.RawHTMLBlock', (), {'label': 'Raw HTML block'})}),
        ),
    ]
