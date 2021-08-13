from django import forms

from v1.models import Feedback


class FeedbackForm(forms.ModelForm):
    """For feedback modules that simply ask 'Was this page helfpul?'"""
    class Meta:
        model = Feedback
        fields = ['is_helpful', 'comment', 'language']

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['is_helpful'].required = True


class ReferredFeedbackForm(forms.ModelForm):
    """For feedback modules that need to capture the referring page"""
    class Meta:
        model = Feedback
        fields = ['is_helpful', 'referrer', 'comment', 'language']

    def __init__(self, *args, **kwargs):
        super(ReferredFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required = True


class SuggestionFeedbackForm(forms.ModelForm):
    """For feedback modules seeking content suggestions"""

    class Meta:
        model = Feedback
        fields = ['referrer',
                  'comment',
                  'expect_to_buy',
                  'currently_own',
                  'email',
                  'language']

    def __init__(self, *args, **kwargs):
        super(SuggestionFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required = True
