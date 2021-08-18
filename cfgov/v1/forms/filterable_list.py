from collections import Counter
from datetime import date

from django import forms
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.utils import timezone

from v1.models import enforcement_action_page
from v1.util import ERROR_MESSAGES, ref
from v1.util.categories import clean_categories
from v1.util.datetimes import end_of_time_period


class FilterableDateField(forms.DateField):
    def validate_after_1900(date):
        strftime_earliest_year = 1900
        if date.year < strftime_earliest_year:
            raise ValidationError("Please enter a date of 1/1/1900 or later.")

    default_validators = [validate_after_1900]

    default_input_formats = (
        '%m/%d/%y',     # 10/25/16, 9/1/16
        '%d/%m/%y',     # 13/4/21
        '%m-%d-%y',     # 10-25-16, 9-1-16
        '%d-%m-%y',     # 13-4-21
        '%m/%d/%Y',     # 10/25/2016, 9/1/2016
        '%d/%m/%Y',     # 13/4/2021
        '%m-%d-%Y',     # 10-25-2016, 9-1-2016
        '%d-%m-%Y',     # 13-4-2021
        '%Y-%m-%d',     # 2016-10-25, 2016-9-1
        '%m/%Y',        # 10/2016, 7/2017
        '%m-%Y',        # 10-2016, 7-2017
        '%m/%y',        # 10/16, 4/18
        '%m-%y',        # 10-16, 4-18
        '%Y',           # 2016
    )

    default_widget_attrs = {
        'class': 'a-text-input a-text-input__full',
        'type': 'date',
        'placeholder': 'mm/dd/yyyy',
        'data-type': 'date'
    }

    def __init__(self, *args, is_end_date=False, **kwargs):
        self.is_end_date = is_end_date

        kwargs.setdefault('required', False)
        kwargs.setdefault('input_formats', self.default_input_formats)
        kwargs.setdefault('error_messages', ERROR_MESSAGES['DATE_ERRORS'])

        field_id = kwargs.pop('field_id', None)
        if field_id:
            self.default_widget_attrs['id'] = field_id

        kwargs.setdefault('widget', widgets.DateInput(
            attrs=self.default_widget_attrs
        ))

        super().__init__(*args, **kwargs)

    def clean(self, value):
        cleaned = super().clean(value)

        if isinstance(value, str) and self.is_end_date:
            return end_of_time_period(value, cleaned)
        else:
            return cleaned


class FilterableListForm(forms.Form):
    title = forms.CharField(
        max_length=250,
        required=False,
        empty_value=None,
        widget=forms.TextInput(attrs={
            'id': 'o-filterable-list-controls_title',
            'class': 'a-text-input a-text-input__full',
        })
    )
    from_date = FilterableDateField(
        field_id='o-filterable-list-controls_from-date'
    )

    to_date = FilterableDateField(
        field_id='o-filterable-list-controls_to-date',
        is_end_date=True
    )

    categories = forms.MultipleChoiceField(
        required=False,
        choices=ref.page_type_choices,
        widget=widgets.SelectMultiple(attrs={
            'id': 'o-filterable-list-controls_categories',
            'class': 'o-multiselect',
            'data-placeholder': 'Search for categories',
            'multiple': 'multiple',
        })
    )

    topics = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=widgets.SelectMultiple(attrs={
            'id': 'o-filterable-list-controls_topics',
            'class': 'o-multiselect',
            'data-placeholder': 'Search for topics',
            'multiple': 'multiple',
        })
    )

    language = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=widgets.SelectMultiple(attrs={
            'id': 'o-filterable-list-controls_language',
            'class': 'o-multiselect',
            'data-placeholder': 'Search for language',
            'multiple': 'multiple',
        })
    )

    archived = forms.ChoiceField(
        required=False,
        choices=[
            ('include', 'Show all items (default)'),
            ('exclude', 'Exclude archived items'),
            ('only', 'Show only archived items'),
        ]
    )

    preferred_datetime_format = '%Y-%m-%d'

    def __init__(self, *args, categories=None, topics=None, languages=None,
        from_date_min=None, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.fields['categories'].choices = categories or []
        self.fields['topics'].choices = topics or []
        self.fields['language'].choices = languages or []

        self.from_date_min = from_date_min

        # clean_categories(selected_categories=self.data.get('categories'))

    def clean(self):
        if self.errors.get('from_date') or self.errors.get('to_date'):
            return self.cleaned_data

        from_date = self.cleaned_data.get('from_date')
        to_date = self.cleaned_data.get('to_date')

        if from_date and to_date:
            if to_date < from_date:
                self.cleaned_data['from_date'] = to_date
                self.cleaned_data['to_date'] = from_date
        elif from_date:
            self.cleaned_data['to_date'] = timezone.now().date()
        elif to_date:
            self.cleaned_data['from_date'] = self.from_date_min

    def clean_archived(self):
        data = self.cleaned_data['archived']
        if data == 'exclude':
            return ['no', 'never']
        elif data == 'only':
            return ['yes']


class EnforcementActionsFilterForm(FilterableListForm):
    statuses = forms.MultipleChoiceField(
        required=False,
        choices=enforcement_action_page.enforcement_statuses,
        widget=widgets.SelectMultiple(attrs={
            'id': 'o-filterable-list-controls_statuses',
            'class': 'o-multiselect',
            'data-placeholder': 'Search for statuses',
            'multiple': 'multiple',
        })
    )

    products = forms.MultipleChoiceField(
        required=False,
        choices=enforcement_action_page.enforcement_products,
        widget=widgets.SelectMultiple(attrs={
            'id': 'o-filterable-list-controls_products',
            'class': 'o-multiselect',
            'data-placeholder': 'Search for products',
            'multiple': 'multiple',
        })
    )
