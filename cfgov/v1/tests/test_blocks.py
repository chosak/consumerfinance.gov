from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase
from django.test.client import RequestFactory
from django.utils.safestring import SafeText

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.models import Page

import mock

from v1.blocks import (
    AbstractFormBlock, AnchorLink, Link, PlaceholderCharBlock, StreamBlock
)


class TestAbstractFormBlock(TestCase):
    def setUp(self):
        self.page = mock.Mock()
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.block_value = mock.Mock()
        self.block = AbstractFormBlock()

    @mock.patch('v1.blocks.AbstractFormBlock.get_handler_class')
    def test_get_result_calls_get_handler_class(self, mock_getclass):
        self.block.get_result(self.page, self.request, self.block_value, True)
        self.assertTrue(mock_getclass.called)

    @mock.patch('v1.blocks.AbstractFormBlock.get_handler_class')
    def test_get_result_instantiates_class(self, mock_getclass):
        self.block.get_result(self.page, self.request, self.block_value, True)
        mock_getclass()().process.assert_called_with(True)

    def test_get_handler_class_raises_AttributeError_for_unset_handler_meta(self):
        with self.assertRaises(AttributeError) as e:
            self.block.get_handler_class()

    @mock.patch('v1.blocks.import_string')
    def test_get_handler_class_returns_load_class_with_handler_path(self, mock_import):
        self.block.meta.handler = 'handler.dot.path'
        self.block.get_handler_class()
        mock_import.assert_called_with(self.block.meta.handler)

    def test_is_submitted_returns_False_for_wrong_method(self):
        result = self.block.is_submitted(self.request, 'name', 0)
        self.assertFalse(result)

    def test_is_submitted_returns_False_if_form_id_doesnt_match(self):
        self.request = self.factory.post('/', {'form_id': 'notamatch-0'})
        result = self.block.is_submitted(self.request, 'withthis', 0)
        self.assertFalse(result)

    def test_is_submitted_returns_True_for_matching_form_id(self):
        self.request = self.factory.post('/', {'form_id': 'form-match-0'})
        result = self.block.is_submitted(self.request, 'match', 0)
        self.assertTrue(result)


class TestAnchorLink(TestCase):
    def setUp(self):
        self.block = AnchorLink()

    def stringContainsNumbers(self, string):
        return any(char.isdigit() for char in string)

    @mock.patch('v1.blocks.AnchorLink.clean')
    def test_clean_calls_format_id(self, mock_format_id):
        self.data = {'link_id': 'test-string'}
        self.block.clean(self.data)
        self.assertTrue(mock_format_id.called)

    def test_clean_called_with_empty_data(self):
        self.data = {'link_id': ''}
        result = self.block.clean(self.data)
        prefix, suffix = result['link_id'].split('_')

        assert 'anchor_' in result['link_id']
        assert prefix == 'anchor'
        assert self.stringContainsNumbers(suffix)

    def test_clean_called_with_string(self):
        self.data = {'link_id': 'kittens playing with string'}
        result = self.block.clean(self.data)
        assert 'anchor_kittens-playing-with-string_' in result['link_id']

    def test_clean_called_with_existing_anchor(self):
        self.data = {'link_id': 'anchor_3472e83b2dd084'}
        result = self.block.clean(self.data)
        assert result['link_id'] == 'anchor_3472e83b2dd084'

    def test_clean_called_with_literally_anchor(self):
        self.data = {'link_id': 'anchor'}
        result = self.block.clean(self.data)

        assert 'anchor_' in result['link_id']
        assert self.stringContainsNumbers(result['link_id'])


class TestPlaceholderBlock(TestCase):
    def test_render_no_placeholder_provided(self):
        block = PlaceholderCharBlock()
        html = block.render_form('Hello world!')
        self.assertInHTML(
            (
                '<input id="" name="" placeholder="" '
                'type="text" value="Hello world!" />'
            ),
            html
        )

    def test_render_no_placeholder_returns_safetext(self):
        block = PlaceholderCharBlock()
        html = block.render_form('Hello world!')
        self.assertIsInstance(html, SafeText)

    def test_render_with_placeholder(self):
        block = PlaceholderCharBlock(placeholder='Hi there!')
        html = block.render_form('Hello world!')
        self.assertIn(
            (
                '<input id="" name="" placeholder="Hi there!" '
                'type="text" value="Hello world!"/>'
            ),
            html
        )

    def test_render_returns_safetext(self):
        block = PlaceholderCharBlock(placeholder='Hi there!')
        html = block.render_form('Hello world!')
        self.assertIsInstance(html, SafeText)

    def test_replace_placeholder(self):
        html = '<input id="foo" placeholder="a" />'
        replaced = PlaceholderCharBlock.replace_placeholder(html, 'b')
        self.assertEqual(replaced, '<input id="foo" placeholder="b"/>')

    def test_replace_placeholder_quotes(self):
        html = '<input id="foo" placeholder="&quot;a&quot;" />'
        replaced = PlaceholderCharBlock.replace_placeholder(html, '"b"')
        self.assertEqual(replaced, '<input id="foo" placeholder=\'"b"\'/>')

    def test_replace_placeholder_no_placeholder(self):
        html = '<input id="foo" />'
        replaced = PlaceholderCharBlock.replace_placeholder(html, 'a')
        self.assertEqual(replaced, '<input id="foo" placeholder="a"/>')

    def test_no_inputs_raises_valueerror(self):
        html = '<div>something</div>'
        with self.assertRaises(ValueError):
            PlaceholderCharBlock.replace_placeholder(html, 'a')

    def test_multiple_inputs_raises_valueerror(self):
        html = '<input id="foo" /><input id="bar" />'
        with self.assertRaises(ValueError):
            PlaceholderCharBlock.replace_placeholder(html, 'a')


class TestLink(TestCase):
    def test_link_with_external_url_validates(self):
        block = Link()
        value = block.to_python(
            {'link_text': 'Link', 'external_link': '/path'}
        )
        try:
            block.clean(value)
        except ValidationError:
            self.fail('Link with url should not fail validation')

    def test_link_without_external_or_page_link_fails(self):
        block = Link()
        value = block.to_python({'link_text': 'Link'})
        with self.assertRaises(ValidationError):
            block.clean(value)


class ConfigurableTextBlock(blocks.StructBlock):
    text = blocks.CharBlock()
    has_top_border = blocks.BooleanBlock()
    has_top_rule_line = blocks.BooleanBlock()
    has_rule = blocks.BooleanBlock()
    has_bottom_border = blocks.BooleanBlock()

    def render(self, value, context=None):
        return value['text']


class SimpleStreamBlock(StreamBlock):
    text = ConfigurableTextBlock()

    def make_text_value(self, text_block_values):
        return self.to_python(list(
            {'type': 'text', 'value': value}
            for value in text_block_values
        ))


class StreamBlockTests(SimpleTestCase):
    def test_render_basic(self):
        block = SimpleStreamBlock()
        value = block.make_text_value([
            {'text': 'foo'},
            {'text': 'bar'},
        ])

        # Each block should render with class="block".
        # The first block should get block__flush-top as well.
        self.assertEqual(block.render(value), '''\
<div class="block block__flush-top">
    foo
</div>
<div class="block">
    bar
</div>
''')

    def test_render_has_top_border(self):
        block = SimpleStreamBlock()
        value = block.make_text_value([
            {'text': 'foo', 'has_top_border': True},
            {'text': 'bar', 'has_top_border': True},
            {'text': 'baz'},
        ])

        # If the first block has has_top_border, don't add block__flush-top.
        # Add block__padded-top and block__border-top wherever it is set.
        self.assertEqual(block.render(value), '''\
<div class="block block__padded-top block__border-top">
    foo
</div>
<div class="block block__padded-top block__border-top">
    bar
</div>
<div class="block">
    baz
</div>
''')

    def test_render_has_top_rule_line(self):
        block = SimpleStreamBlock()
        value = block.make_text_value([
            {'text': 'foo', 'has_top_rule_line': True},
            {'text': 'bar', 'has_top_rule_line': True},
            {'text': 'baz'},
        ])

        # If the first block has has_top_rule_line, don't add block__flush-top.
        # Add block__padded-top and block__border-top wherever it is set.
        self.assertEqual(block.render(value), '''\
<div class="block block__padded-top block__border-top">
    foo
</div>
<div class="block block__padded-top block__border-top">
    bar
</div>
<div class="block">
    baz
</div>
''')

    def test_render_has_top_border_and_has_top_rule_line(self):
        block = SimpleStreamBlock()
        value = block.make_text_value([
            {'text': 'foo', 'has_top_border': True, 'has_top_rule_line': True},
        ])

        # If both has_top_border and has_top_rule_line are set, the classes
        # block__padded-top and block__border-top should only be added once.
        self.assertEqual(block.render(value), '''\
<div class="block block__padded-top block__border-top">
    foo
</div>
''')

    def test_render_has_rule(self):
        block = SimpleStreamBlock()
        value = block.make_text_value([
            {'text': 'foo', 'has_rule': True},
            {'text': 'bar'},
            {'text': 'baz', 'has_rule': True},
        ])

        # Add block__padded-bottom and block__border-bottom to any block
        # that has has_rule set.
        self.assertEqual(block.render(value), '''\
<div class="block block__flush-top block__padded-bottom block__border-bottom">
    foo
</div>
<div class="block">
    bar
</div>
<div class="block block__padded-bottom block__border-bottom">
    baz
</div>
''')

    def test_render_has_bottom_border(self):
        block = SimpleStreamBlock()
        value = block.make_text_value([
            {'text': 'foo', 'has_bottom_border': True},
            {'text': 'bar'},
            {'text': 'baz', 'has_bottom_border': True},
        ])

        # Add block__padded-bottom and block__border-bottom to any block
        # that has has_bottom_border set.
        self.assertEqual(block.render(value), '''\
<div class="block block__flush-top block__padded-bottom block__border-bottom">
    foo
</div>
<div class="block">
    bar
</div>
<div class="block block__padded-bottom block__border-bottom">
    baz
</div>
''')

    def test_render_has_rule_and_has_bottom_border(self):
        block = SimpleStreamBlock()
        value = block.make_text_value([
            {'text': 'foo', 'has_rule': True, 'has_bottom_border': True},
        ])

        # If both has_rule and has_bottom_border are set, the classes
        # block__padded-bottom and block__border-bottom should only be added
        # once.
        self.assertEqual(block.render(value), '''\
<div class="block block__flush-top block__padded-bottom block__border-bottom">
    foo
</div>
''')

    def test_render_block_with_meta_classname(self):
        class MyCharBlock(blocks.CharBlock):
            class Meta:
                classname = 'mine'

        class TestStreamBlock(StreamBlock):
            text = MyCharBlock()

        block = TestStreamBlock()
        value = block.to_python([{'type': 'text', 'value': 'foo'}])
        self.assertEqual(block.render(value), '''\
<div class="block block__flush-top mine">
    foo
</div>
''')

