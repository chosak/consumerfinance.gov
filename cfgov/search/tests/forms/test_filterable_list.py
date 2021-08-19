from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from freezegun import freeze_time

from search.forms.filterable_list import (
    FilterableDateField, FilterableListForm
)


@freeze_time('2021-08-18')
class TestFilterableListForm(SimpleTestCase):
    def setUp(self):
        self.empty_cleaned_data = {
            'archived': None,
            'categories': [],
            'from_date': None,
            'language': [],
            'title': None,
            'to_date': None,
            'topics': [],
        }

    def make_cleaned_data(self, kwargs):
        cleaned_data = dict(self.empty_cleaned_data)
        cleaned_data.update(kwargs)
        return cleaned_data

    def test_clean_no_dates(self):
        form = FilterableListForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.empty_cleaned_data)

    def test_clean_uses_today_if_to_date_is_empty(self):
        from_date = date(2010, 1, 1)

        data = {'from_date': from_date}
        form = FilterableListForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.make_cleaned_data({
            'from_date': from_date,
            'to_date': date(2021, 8, 18),
        }))

    def test_clean_both_dates(self):
        from_date = date(2020, 1, 23)
        to_date = from_date + timedelta(weeks=52)

        data = {'from_date': from_date, 'to_date': to_date}
        form = FilterableListForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.make_cleaned_data(data))

    def test_clean_both_dates_in_future(self):
        from_date = date(2048, 1, 23)
        to_date = from_date + timedelta(weeks=52)

        data = {'from_date': from_date, 'to_date': to_date}
        form = FilterableListForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.make_cleaned_data(data))

    def test_clean_switches_date_fields_if_to_date_before_from_date(self):
        to_date = date(2000, 3, 15)
        from_date = to_date + timedelta(days=1)

        data = {'from_date': from_date, 'to_date': to_date}
        form = FilterableListForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.make_cleaned_data({
            'from_date': to_date,
            'to_date': from_date,
        }))

    def test_clean_uses_from_date_min_if_to_date_set_but_not_from_date(self):
        from_date_min = date(2010, 1, 1)
        to_date = date(2020, 1, 1)

        data = {'to_date': to_date}
        form = FilterableListForm(data=data, from_date_min=from_date_min)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.make_cleaned_data({
            'from_date': from_date_min,
            'to_date': to_date,
        }))

    def test_clean_ignores_from_date_min_if_no_dates_set(self):
        from_date_min = date(2010, 1, 1)

        form = FilterableListForm(data={}, from_date_min=from_date_min)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.empty_cleaned_data)

    def test_clean_passes_through_date_validation_errors(self):
        from_date_min = date(2010, 1, 1)
        to_date = 'this is not a date and should fail validation'

        data = {'to_date': to_date}
        form = FilterableListForm(data=data, from_date_min=from_date_min)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'to_date': ['You have entered an invalid date.'],
        })

    def check_clean_archived(self, value, expected_cleaned_value):
        form = FilterableListForm(data={'archived': value})

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data,
            self.make_cleaned_data({'archived': expected_cleaned_value})
        )

    def test_clean_archived_include(self):
        self.check_clean_archived('include', None)

    def test_clean_archived_exclude(self):
        self.check_clean_archived('exclude', ['no', 'never'])

    def test_clean_archived_only(self):
        self.check_clean_archived('only', ['yes'])


class TestFilterableDateField(SimpleTestCase):
    def test_default_required(self):
        field = FilterableDateField()
        self.assertFalse(field.required)

    def test_set_required(self):
        field = FilterableDateField(required=True)
        self.assertTrue(field.required)

    TEST_DATES = [
        ('10/25/16', date(2016, 10, 25)),
        ('13/4/21', date(2021, 4, 13)),
        ('10-25-16', date(2016, 10, 25)),
        ('2016-10-25', date(2016, 10, 25)),
    ]

    def test_clean_default_behavior(self):
        field = FilterableDateField()

        for text, value in self.TEST_DATES + [
            ('10-2016', date(2016, 10, 1)),
            ('2016', date(2016, 1, 1)),
        ]:
            self.assertEqual(field.clean(text), value)

    def test_clean_is_end_date_behavior(self):
        field = FilterableDateField(is_end_date=True)

        for text, value in self.TEST_DATES + [
            ('10-2016', date(2016, 10, 31)),
            ('2016', date(2016, 12, 31)),
        ]:
            self.assertEqual(field.clean(text), value)

    def test_validation_fails_on_dates_before_1900(self):
        with self.assertRaises(ValidationError):
            FilterableDateField().clean('1899-12-31')

    def test_validation_fails_on_dates_before_1900_is_end_date(self):
        with self.assertRaises(ValidationError):
            FilterableDateField(is_end_date=True).clean('1899')
