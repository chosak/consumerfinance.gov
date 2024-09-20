# Generated by Django 4.2.16 on 2024-09-20 17:26

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('regulations3k', '0011_add_footnotes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regulationlandingpage',
            name='content',
            field=wagtail.fields.StreamField([('notification', 9), ('full_width_text', 50)], blank=True, block_lookup={0: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('information', 'Information'), ('warning', 'Warning')]}), 1: ('wagtail.blocks.CharBlock', (), {'help_text': 'The main notification message to display.', 'required': True}), 2: ('wagtail.blocks.TextBlock', (), {'help_text': 'Explanation text appears below the message in smaller type.', 'required': False}), 3: ('wagtail.blocks.CharBlock', (), {'required': False}), 4: ('wagtail.blocks.CharBlock', (), {'help_text': 'Add an ARIA label if the link text does not describe the destination of the link (e.g. has ambiguous text like "Learn more" that is not descriptive on its own).', 'required': False}), 5: ('wagtail.blocks.CharBlock', (), {'default': '/', 'required': False}), 6: ('wagtail.blocks.BooleanBlock', (), {'default': False, 'required': False}), 7: ('wagtail.blocks.StructBlock', [[('text', 3), ('aria_label', 4), ('url', 5), ('is_link_boldface', 6)]], {}), 8: ('wagtail.blocks.ListBlock', (7,), {'help_text': 'Links appear on their own lines below the explanation.', 'required': False}), 9: ('wagtail.blocks.StructBlock', [[('type', 0), ('message', 1), ('explanation', 2), ('links', 8)]], {}), 10: ('wagtail.blocks.RichTextBlock', (), {'icon': 'edit'}), 11: ('wagtail.blocks.RichTextBlock', (), {}), 12: ('wagtail.blocks.CharBlock', (), {'help_text': '\n            ID will be auto-generated on save.\n            However, you may enter some human-friendly text that\n            will be incorporated to make it easier to read.\n        ', 'label': 'ID for this content block', 'required': False}), 13: ('wagtail.blocks.StructBlock', [[('link_id', 12)]], {}), 14: ('wagtail.blocks.StructBlock', [[('content_block', 11), ('anchor_link', 13)]], {}), 15: ('wagtail_footnotes.blocks.RichTextBlockWithFootnotes', (), {'features': ['anchor-identifier', 'h2', 'h3', 'h4', 'h5', 'hr', 'ol', 'ul', 'bold', 'italic', 'superscript', 'blockquote', 'link', 'document-link', 'image', 'icon', 'footnotes']}), 16: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5')]}), 17: ('wagtail.blocks.CharBlock', (), {'help_text': 'Input the name of an icon to appear to the left of the heading. E.g., approved, help-round, etc. <a href="https://cfpb.github.io/design-system/foundation/iconography">See full list of icons</a>', 'required': False}), 18: ('wagtail.blocks.StructBlock', [[('text', 3), ('level', 16), ('icon', 17)]], {'required': False}), 19: ('wagtail.images.blocks.ImageChooserBlock', (), {'required': False}), 20: ('wagtail.blocks.CharBlock', (), {'help_text': "No character limit, but be as succinct as possible. If the image is decorative (i.e., a screenreader wouldn't have anything useful to say about it), leave this field blank.", 'required': False}), 21: ('wagtail.blocks.StructBlock', [[('upload', 19), ('alt', 20)]], {}), 22: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('full', 'Full width'), (470, '470px'), (270, '270px'), (170, '170px')]}), 23: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('right', 'right'), ('left', 'left')], 'help_text': 'Does not apply if the image is full-width'}), 24: ('wagtail.blocks.RichTextBlock', (), {'label': 'Caption', 'required': False}), 25: ('wagtail.blocks.BooleanBlock', (), {'default': True, 'help_text': 'Check to add a horizontal rule line to bottom of inset.', 'label': 'Has bottom rule line', 'required': False}), 26: ('wagtail.blocks.StructBlock', [[('image', 21), ('image_width', 22), ('image_position', 23), ('text', 24), ('is_bottom_rule', 25)]], {}), 27: ('wagtail.blocks.MultipleChoiceBlock', [], {'choices': [('is_full_width', 'Display the table at full width'), ('stack_on_mobile', 'Stack the table columns on mobile')], 'required': False}), 28: ('wagtail.blocks.CharBlock', (), {}), 29: ('wagtail.blocks.FloatBlock', (), {}), 30: ('wagtail.blocks.RichTextBlock', (), {'features': ['bold', 'italic', 'ol', 'ul', 'link', 'document-link', 'superscript']}), 31: ('wagtail_footnotes.blocks.RichTextBlockWithFootnotes', (), {'features': ['bold', 'italic', 'ol', 'ul', 'link', 'document-link', 'superscript', 'footnotes']}), 32: ('wagtail.contrib.typed_table_block.blocks.TypedTableBlock', [[('text', 28), ('numeric', 29), ('rich_text', 30), ('rich_text_with_footnotes', 31)]], {}), 33: ('wagtail.blocks.RichTextBlock', (), {'required': False}), 34: ('wagtail.blocks.StructBlock', [[('heading', 18), ('text_introduction', 3), ('options', 27), ('data', 32), ('caption', 33)]], {}), 35: ('wagtail.blocks.TextBlock', (), {}), 36: ('wagtail.blocks.TextBlock', (), {'required': False}), 37: ('wagtail.blocks.StructBlock', [[('body', 35), ('citation', 36)]], {}), 38: ('wagtail.blocks.StructBlock', [[('slug_text', 3), ('paragraph_text', 33), ('button', 7)]], {}), 39: ('wagtail.blocks.ListBlock', (7,), {}), 40: ('wagtail.blocks.StructBlock', [[('heading', 3), ('paragraph', 33), ('links', 39)]], {}), 41: ('v1.blocks.ReusableTextChooserBlock', ('v1.ReusableText',), {}), 42: ('v1.blocks.ReusableNotificationChooserBlock', ('v1.ReusableNotification',), {}), 43: ('v1.blocks.EmailSignUpChooserBlock', (), {}), 44: ('wagtail.blocks.RichTextBlock', (), {'label': 'Well', 'required': False}), 45: ('wagtail.blocks.StructBlock', [[('content', 44)]], {}), 46: ('wagtail.blocks.CharBlock', (), {'help_text': 'Regulations list heading', 'required': False}), 47: ('wagtail.blocks.PageChooserBlock', (), {'help_text': 'Link to more regulations'}), 48: ('wagtail.blocks.CharBlock', (), {'help_text': 'Text to show on link to more regulations', 'required': False}), 49: ('wagtail.blocks.StructBlock', [[('heading', 46), ('more_regs_page', 47), ('more_regs_text', 48)]], {}), 50: ('wagtail.blocks.StreamBlock', [[('content', 10), ('content_with_anchor', 14), ('content_with_footnotes', 15), ('heading', 18), ('image', 26), ('table', 34), ('quote', 37), ('cta', 38), ('related_links', 40), ('reusable_text', 41), ('reusable_notification', 42), ('email_signup', 43), ('well', 45), ('regulations_list', 49)]], {})}),
        ),
        migrations.AlterField(
            model_name='regulationpage',
            name='content',
            field=wagtail.fields.StreamField([('info_unit_group', 22), ('full_width_text', 52)], blank=True, block_lookup={0: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('50-50', '50/50'), ('33-33-33', '33/33/33'), ('25-75', '25/75')], 'help_text': 'Choose the number and width of info unit columns.', 'label': 'Format'}), 1: ('wagtail.blocks.CharBlock', (), {'required': False}), 2: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5')]}), 3: ('wagtail.blocks.CharBlock', (), {'help_text': 'Input the name of an icon to appear to the left of the heading. E.g., approved, help-round, etc. <a href="https://cfpb.github.io/design-system/foundation/iconography">See full list of icons</a>', 'required': False}), 4: ('wagtail.blocks.StructBlock', [[('text', 1), ('level', 2), ('icon', 3)]], {'required': False}), 5: ('wagtail.blocks.RichTextBlock', (), {'required': False}), 6: ('wagtail.blocks.BooleanBlock', (), {'default': True, 'help_text': "Check this to link all images and headings to the URL of the first link in their unit's list, if there is a link.", 'required': False}), 7: ('wagtail.blocks.BooleanBlock', (), {'default': False, 'help_text': 'Check this to add a horizontal rule line to top of info unit group.', 'required': False}), 8: ('wagtail.blocks.BooleanBlock', (), {'default': False, 'help_text': 'Check this to show horizontal rule lines between info units.', 'label': 'Show rule lines between items', 'required': False}), 9: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('none', 'None'), ('rounded', 'Rounded corners'), ('circle', 'Circle')], 'help_text': 'Adds a <em>border-radius</em> class to images in this group, allowing for a rounded or circular border.', 'label': 'Border radius for images?', 'required': False}), 10: ('wagtail.images.blocks.ImageChooserBlock', (), {'required': False}), 11: ('wagtail.blocks.CharBlock', (), {'help_text': "No character limit, but be as succinct as possible. If the image is decorative (i.e., a screenreader wouldn't have anything useful to say about it), leave this field blank.", 'required': False}), 12: ('wagtail.blocks.StructBlock', [[('upload', 10), ('alt', 11)]], {}), 13: ('wagtail.blocks.StructBlock', [[('text', 1), ('level', 2), ('icon', 3)]], {'default': {'level': 'h3'}, 'required': False}), 14: ('wagtail.blocks.RichTextBlock', (), {'blank': True, 'required': False}), 15: ('wagtail.blocks.CharBlock', (), {'help_text': 'Add an ARIA label if the link text does not describe the destination of the link (e.g. has ambiguous text like "Learn more" that is not descriptive on its own).', 'required': False}), 16: ('wagtail.blocks.CharBlock', (), {'default': '/', 'required': False}), 17: ('wagtail.blocks.BooleanBlock', (), {'default': False, 'required': False}), 18: ('wagtail.blocks.StructBlock', [[('text', 1), ('aria_label', 15), ('url', 16), ('is_link_boldface', 17)]], {}), 19: ('wagtail.blocks.ListBlock', (18,), {'required': False}), 20: ('wagtail.blocks.StructBlock', [[('image', 12), ('heading', 13), ('body', 14), ('links', 19)]], {}), 21: ('wagtail.blocks.ListBlock', (20,), {'default': []}), 22: ('wagtail.blocks.StructBlock', [[('format', 0), ('heading', 4), ('intro', 5), ('link_image_and_heading', 6), ('has_top_rule_line', 7), ('lines_between_items', 8), ('border_radius_image', 9), ('info_units', 21)]], {}), 23: ('wagtail.blocks.RichTextBlock', (), {'icon': 'edit'}), 24: ('wagtail.blocks.RichTextBlock', (), {}), 25: ('wagtail.blocks.CharBlock', (), {'help_text': '\n            ID will be auto-generated on save.\n            However, you may enter some human-friendly text that\n            will be incorporated to make it easier to read.\n        ', 'label': 'ID for this content block', 'required': False}), 26: ('wagtail.blocks.StructBlock', [[('link_id', 25)]], {}), 27: ('wagtail.blocks.StructBlock', [[('content_block', 24), ('anchor_link', 26)]], {}), 28: ('wagtail_footnotes.blocks.RichTextBlockWithFootnotes', (), {'features': ['anchor-identifier', 'h2', 'h3', 'h4', 'h5', 'hr', 'ol', 'ul', 'bold', 'italic', 'superscript', 'blockquote', 'link', 'document-link', 'image', 'icon', 'footnotes']}), 29: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('full', 'Full width'), (470, '470px'), (270, '270px'), (170, '170px')]}), 30: ('wagtail.blocks.ChoiceBlock', [], {'choices': [('right', 'right'), ('left', 'left')], 'help_text': 'Does not apply if the image is full-width'}), 31: ('wagtail.blocks.RichTextBlock', (), {'label': 'Caption', 'required': False}), 32: ('wagtail.blocks.BooleanBlock', (), {'default': True, 'help_text': 'Check to add a horizontal rule line to bottom of inset.', 'label': 'Has bottom rule line', 'required': False}), 33: ('wagtail.blocks.StructBlock', [[('image', 12), ('image_width', 29), ('image_position', 30), ('text', 31), ('is_bottom_rule', 32)]], {}), 34: ('wagtail.blocks.MultipleChoiceBlock', [], {'choices': [('is_full_width', 'Display the table at full width'), ('stack_on_mobile', 'Stack the table columns on mobile')], 'required': False}), 35: ('wagtail.blocks.CharBlock', (), {}), 36: ('wagtail.blocks.FloatBlock', (), {}), 37: ('wagtail.blocks.RichTextBlock', (), {'features': ['bold', 'italic', 'ol', 'ul', 'link', 'document-link', 'superscript']}), 38: ('wagtail_footnotes.blocks.RichTextBlockWithFootnotes', (), {'features': ['bold', 'italic', 'ol', 'ul', 'link', 'document-link', 'superscript', 'footnotes']}), 39: ('wagtail.contrib.typed_table_block.blocks.TypedTableBlock', [[('text', 35), ('numeric', 36), ('rich_text', 37), ('rich_text_with_footnotes', 38)]], {}), 40: ('wagtail.blocks.StructBlock', [[('heading', 4), ('text_introduction', 1), ('options', 34), ('data', 39), ('caption', 5)]], {}), 41: ('wagtail.blocks.TextBlock', (), {}), 42: ('wagtail.blocks.TextBlock', (), {'required': False}), 43: ('wagtail.blocks.StructBlock', [[('body', 41), ('citation', 42)]], {}), 44: ('wagtail.blocks.StructBlock', [[('slug_text', 1), ('paragraph_text', 5), ('button', 18)]], {}), 45: ('wagtail.blocks.ListBlock', (18,), {}), 46: ('wagtail.blocks.StructBlock', [[('heading', 1), ('paragraph', 5), ('links', 45)]], {}), 47: ('v1.blocks.ReusableTextChooserBlock', ('v1.ReusableText',), {}), 48: ('v1.blocks.ReusableNotificationChooserBlock', ('v1.ReusableNotification',), {}), 49: ('v1.blocks.EmailSignUpChooserBlock', (), {}), 50: ('wagtail.blocks.RichTextBlock', (), {'label': 'Well', 'required': False}), 51: ('wagtail.blocks.StructBlock', [[('content', 50)]], {}), 52: ('wagtail.blocks.StreamBlock', [[('content', 23), ('content_with_anchor', 27), ('content_with_footnotes', 28), ('heading', 4), ('image', 33), ('table', 40), ('quote', 43), ('cta', 44), ('related_links', 46), ('reusable_text', 47), ('reusable_notification', 48), ('email_signup', 49), ('well', 51)]], {})}, null=True),
        ),
    ]
