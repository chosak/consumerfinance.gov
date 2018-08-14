from django.test import RequestFactory, TestCase, override_settings

from legacy.views.complaint import ComplaintLandingView

import responses


class ComplaintLandingViewTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/')

    def assertNoBanner(self, response):
        self.assertNotContains(response, 'show-')

    @override_settings(COMPLAINT_LANDING_STATUS_SOURCE=None)
    def test_no_stats_source(self):
        response = ComplaintLandingView.as_view()(self.request)
        self.assertNoBanner(response)

    @responses.activate
    @override_settings(COMPLAINT_LANDING_STATUS_SOURCE='https://test.url/foo.json')
    def test_data_out_of_date(self):
        responses.add(responses.GET, 'https://test.url/foo.json', json={
            'stats': {
                'last_updated': '2010-01-01',
                'last_updated_narratives': '2010-01-01',
            },
        })
        response = ComplaintLandingView.as_view()(self.request)
        self.assertContains(response, 'show-data-notification')
