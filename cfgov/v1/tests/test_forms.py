from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase
from django.utils.text import slugify

from wagtail.images.forms import get_image_form

from freezegun import freeze_time
from taggit.models import Tag

from v1.forms import FilterableDateField, FilterableListForm
from v1.models import CFGOVImage


def make_filterable_list_form(**kwargs):
    data = {
        "default_min_date": date(2020, 1, 1),
        "topic_slugs": [],
        "language_codes": [],
    }

    data.update(**kwargs)

    return FilterableListForm(**data)


class TestFilterableListFormTopics(TestCase):
    def test_topic_choices(self):
        Tag.objects.bulk_create(
            [Tag(slug=slugify(text), name=text) for text in ("Foo", "Bar")]
        )

        form = make_filterable_list_form(topic_slugs=["foo", "bar", "extra"])

        self.assertEqual(
            form.fields["topics"].choices,
            [
                ("bar", "Bar"),
                ("foo", "Foo"),
            ],
        )


class TestFilterableListForm(SimpleTestCase):
    def test_language_codes(self):
        form = make_filterable_list_form(language_codes=["es", "en", "ar"])

        self.assertEqual(
            form.fields["language"].choices,
            [("ar", "Arabic"), ("en", "English"), ("es", "Spanish")],
        )

    def test_clean_from_and_to_date(self):
        form = make_filterable_list_form(
            data={"from_date": "7/4/2017", "to_date": "7/5/2017"}
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["from_date"], date(2017, 7, 4))
        self.assertEqual(form.cleaned_data["to_date"], date(2017, 7, 5))

    def test_from_date_uses_default_if_not_provided(self):
        form = make_filterable_list_form(
            default_min_date=date(2020, 1, 1),
            data={"to_date": "12/25/2022"},
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["from_date"], date(2020, 1, 1))
        self.assertEqual(form.cleaned_data["to_date"], date(2022, 12, 25))

    @freeze_time("2023-05-01")
    def test_to_date_uses_today_if_not_provided(self):
        form = make_filterable_list_form(data={"from_date": "7/4/2017"})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["from_date"], date(2017, 7, 4))
        self.assertEqual(form.cleaned_data["to_date"], date(2023, 5, 1))

    def test_both_dates_are_none_if_not_provided(self):
        form = make_filterable_list_form(data={"title": "Test"})

        self.assertTrue(form.is_valid())
        self.assertIsNone(form.cleaned_data["from_date"])
        self.assertIsNone(form.cleaned_data["to_date"])

    def test_switches_dates_if_swapped(self):
        form = make_filterable_list_form(
            data={"from_date": "7/5/2017", "to_date": "7/4/2017"}
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["from_date"], date(2017, 7, 4))
        self.assertEqual(form.cleaned_data["to_date"], date(2017, 7, 5))

    def test_propogates_date_errors(self):
        form = make_filterable_list_form(
            data={"from_date": "7/5/2017", "to_date": "elephant"}
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors, {"to_date": ["You have entered an invalid date."]}
        )

    def test_should_index_unbound(self):
        form = make_filterable_list_form()
        self.assertFalse(form.do_not_index)

    def test_should_index_empty_data(self):
        form = make_filterable_list_form(data={})
        self.assertFalse(form.do_not_index)

    def test_do_not_index_filtered_by_title(self):
        form = make_filterable_list_form(data={"title": "test"})
        self.assertTrue(form.do_not_index)

    def test_should_index_filtered_by_single_topic(self):
        form = make_filterable_list_form(data={"topics": ["foo"]})
        self.assertFalse(form.do_not_index)

    def test_do_not_index_filtered_by_multiple_topics(self):
        form = make_filterable_list_form(data={"topics": ["foo", "bar"]})
        self.assertTrue(form.do_not_index)

    def test_has_active_filters_unbound(self):
        form = make_filterable_list_form()
        self.assertFalse(form.has_active_filters)

    def test_has_active_filters_title(self):
        form = make_filterable_list_form(data={"title": "test"})
        self.assertTrue(form.has_active_filters)

    def test_has_active_filters_title_null_string(self):
        form = make_filterable_list_form(data={"title": None})
        self.assertFalse(form.has_active_filters)

    def test_has_active_filters_title_empty_string(self):
        form = make_filterable_list_form(data={"title": ""})
        self.assertFalse(form.has_active_filters)

    def test_has_active_filters_topics_null(self):
        form = make_filterable_list_form(data={"topics": None})
        self.assertFalse(form.has_active_filters)

    def test_has_active_filters_topics_empty(self):
        form = make_filterable_list_form(data={"topics": []})
        self.assertFalse(form.has_active_filters)

    def test_has_active_filters_topics_single_value(self):
        form = make_filterable_list_form(data={"topics": ["foo"]})
        self.assertTrue(form.has_active_filters)

    def test_has_active_filters_topics_multiple_values(self):
        form = make_filterable_list_form(data={"topics": ["foo", "bar"]})
        self.assertTrue(form.has_active_filters)


class TestFilterableDateField(TestCase):
    def test_default_required(self):
        field = FilterableDateField()
        self.assertFalse(field.required)

    def test_set_required(self):
        field = FilterableDateField(required=True)
        self.assertTrue(field.required)

    def test_clean_valid_date(self):
        self.assertEqual(
            FilterableDateField().clean("1/2/1900"), date(1900, 1, 2)
        )

    def test_rejects_dates_before_1900(self):
        with self.assertRaises(ValidationError):
            FilterableDateField().clean("1/2/1899")


class CFGOVImageFormTests(TestCase):
    def test_alt_widget_override(self):
        form_cls = get_image_form(CFGOVImage)
        form = form_cls()
        self.assertIsInstance(form.fields["alt"].widget, forms.TextInput)
