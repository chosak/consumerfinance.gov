from datetime import date
from operator import itemgetter

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import widgets

from wagtail.images.forms import BaseImageForm

from taggit.models import Tag

from v1.models import enforcement_action_page
from v1.util import ERROR_MESSAGES, ref
from v1.util.datetimes import end_of_time_period


class FilterableDateField(forms.DateField):
    def validate_after_1900(date):
        strftime_earliest_year = 1900
        if date.year < strftime_earliest_year:
            raise ValidationError("Please enter a date of 1/1/1900 or later.")

    default_validators = [validate_after_1900]

    default_input_formats = (
        "%m/%d/%y",  # 10/25/16, 9/1/16
        "%d/%m/%y",  # 13/4/21
        "%m-%d-%y",  # 10-25-16, 9-1-16
        "%d-%m-%y",  # 13-4-21
        "%m/%d/%Y",  # 10/25/2016, 9/1/2016
        "%d/%m/%Y",  # 13/4/2021
        "%m-%d-%Y",  # 10-25-2016, 9-1-2016
        "%d-%m-%Y",  # 13-4-2021
        "%Y-%m-%d",  # 2016-10-25, 2016-9-1
        "%m/%Y",  # 10/2016, 7/2017
        "%m-%Y",  # 10-2016, 7-2017
        "%m/%y",  # 10/16, 4/18
        "%m-%y",  # 10-16, 4-18
        "%Y",  # 2016
    )

    default_widget_attrs = {
        "class": "a-text-input a-text-input__full",
        "type": "date",
        "placeholder": "mm/dd/yyyy",
        "data-type": "date",
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        kwargs.setdefault("input_formats", self.default_input_formats)
        kwargs.setdefault("error_messages", ERROR_MESSAGES["DATE_ERRORS"])

        field_id = kwargs.pop("field_id", None)
        if field_id:
            self.default_widget_attrs["id"] = field_id

        kwargs.setdefault(
            "widget", widgets.DateInput(attrs=self.default_widget_attrs)
        )
        super().__init__(*args, **kwargs)


class FilterableListForm(forms.Form):
    model_class = forms.CharField(required=False, widget=forms.HiddenInput())

    title = forms.CharField(
        max_length=250,
        required=False,
        widget=forms.TextInput(
            attrs={
                "id": "o-filterable-list-controls_title",
                "class": "a-text-input a-text-input__full",
            }
        ),
    )

    from_date = FilterableDateField(
        field_id="o-filterable-list-controls_from-date"
    )

    to_date = FilterableDateField(
        field_id="o-filterable-list-controls_to-date"
    )

    categories = forms.MultipleChoiceField(
        required=False,
        choices=ref.page_type_choices,
        widget=widgets.SelectMultiple(
            attrs={
                "id": "o-filterable-list-controls_categories",
                "class": "o-multiselect",
                "data-placeholder": "Search for categories",
                "multiple": "multiple",
            }
        ),
    )

    topics = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=widgets.SelectMultiple(
            attrs={
                "id": "o-filterable-list-controls_topics",
                "class": "o-multiselect",
                "data-placeholder": "Search for topics",
                "multiple": "multiple",
            }
        ),
    )

    language = forms.MultipleChoiceField(
        required=False,
        choices=[],
        widget=widgets.SelectMultiple(
            attrs={
                "id": "o-filterable-list-controls_language",
                "class": "o-multiselect",
                "data-placeholder": "Search for language",
                "multiple": "multiple",
            }
        ),
    )

    statuses = forms.MultipleChoiceField(
        required=False,
        choices=enforcement_action_page.enforcement_statuses,
        widget=widgets.SelectMultiple(
            attrs={
                "id": "o-filterable-list-controls_statuses",
                "class": "o-multiselect",
                "data-placeholder": "Search for statuses",
                "multiple": "multiple",
            }
        ),
    )

    products = forms.MultipleChoiceField(
        required=False,
        choices=enforcement_action_page.enforcement_products,
        widget=widgets.SelectMultiple(
            attrs={
                "id": "o-filterable-list-controls_products",
                "class": "o-multiselect",
                "data-placeholder": "Search for products",
                "multiple": "multiple",
            }
        ),
    )

    preferred_datetime_format = "%Y-%m-%d"

    def __init__(self, *args, **kwargs):
        self.default_min_date = kwargs.pop("default_min_date")

        topic_choices = self.get_topic_choices(kwargs.pop("topic_slugs"))
        language_choices = self.get_language_choices(
            kwargs.pop("language_codes")
        )

        super().__init__(*args, **kwargs)

        self.fields["topics"].choices = topic_choices
        self.fields["language"].choices = language_choices

    def get_topic_choices(self, topic_slugs):
        return (
            Tag.objects.filter(slug__in=topic_slugs)
            .values_list("slug", "name")
            .order_by("name")
        )

    def get_language_choices(self, language_codes):
        languages = [
            (code, name)
            for code, name in settings.LANGUAGES
            if code in language_codes
        ]

        return sorted(languages, key=itemgetter(1))

    def clean(self):
        cleaned_data = super().clean()
        if self.errors.get("from_date") or self.errors.get("to_date"):
            return cleaned_data
        else:
            ordered_dates = self.order_from_and_to_date_filters(cleaned_data)
            transformed_dates = self.set_interpreted_date_values(ordered_dates)
            return transformed_dates

    def order_from_and_to_date_filters(self, cleaned_data):
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        # Check if both from_date and to_date are present.
        # If the 'start' date is after the 'end' date, swap them.
        if (from_date and to_date) and to_date < from_date:
            self.data = self.data.copy()

            data_to_date = self.data["to_date"]
            self.cleaned_data["to_date"] = from_date
            self.data["to_date"] = self.data["from_date"]

            self.cleaned_data["from_date"] = to_date
            self.data["from_date"] = data_to_date

        return self.cleaned_data

    def set_interpreted_date_values(self, cleaned_data):
        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        # If from_ or to_ is filled in, fill them both with sensible values.
        # If neither is filled in, leave them both blank.
        if from_date or to_date:
            self.data = self.data.copy()

            if from_date:
                self.data["from_date"] = date.strftime(
                    cleaned_data["from_date"], self.preferred_datetime_format
                )
            else:
                # If there's a 'to_date' and no 'from_date',
                #  use default_min_date as 'from_date'.
                default_from_date = min(to_date, self.default_min_date)
                cleaned_data["from_date"] = default_from_date
                self.data["from_date"] = date.strftime(
                    default_from_date, self.preferred_datetime_format
                )

            if to_date:
                self.data["to_date"] = date.strftime(
                    cleaned_data["to_date"], self.preferred_datetime_format
                )
            else:
                # If there's a 'from_date' but no 'to_date', use today's date.
                default_to_date = max(from_date, date.today())
                cleaned_data["to_date"] = default_to_date
                self.data["to_date"] = date.strftime(
                    default_to_date, self.preferred_datetime_format
                )

        return cleaned_data

    @property
    def do_not_index(self):
        """Whether the results from this form should be indexed by crawlers.

        Allow indexing of the form's default state, without any filters.
        Otherwise, do not index queries unless they consist of a single topic
        field.
        """
        if not self.is_bound:
            return False

        if not self.data:
            return False

        if list(self.data.keys()) != ["topics"]:
            return True

        topics = self.data.get("topics")
        return not (isinstance(topics, str) or len(topics) == 1)

    @property
    def has_active_filters(self):
        """Whether this form is being actively filtered by a query."""
        return self.is_bound and any(self.data.values())


class CFGOVImageForm(BaseImageForm):
    """Override the default alt text form widget.

    Our custom image alt text field has no character limit, which renders by
    default as a multi-line textarea field. We instead want to use a
    single-line text input field.
    """

    class Meta(BaseImageForm.Meta):
        widgets = {**BaseImageForm.Meta.widgets, "alt": forms.TextInput}
