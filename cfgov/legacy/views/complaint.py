import requests
import json
from datetime import datetime, date, timedelta
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.conf import settings

from flags.state import (
    flag_state,
    flag_enabled,
    flag_disabled,
)

DEMO_JSON = {"stats": {"percent_timely": 42.0, "last_updated": "2018-01-01", "last_updated_narratives": "2018-01-01"}}

class ComplaintLandingView(TemplateView):
    """
    Main page view.

    To run as a standalone demo with local data, put your demo json
    in the 'demo.json' file at the project root and use this standalone url:
    'http://127.0.0.1:8000/complaintdatabase/demo/demo.json/'
    You can use a different file name; just specify it in the last URL field.
    """

    @property
    def template_name(self):
        return "complaint/complaint-landing.html"

    def get_context_data(self, **kwargs):
        context = super(ComplaintLandingView, self).get_context_data(**kwargs)
        res_json = get_narratives_json()
        context['stats'] = get_stats(res_json)
        (context['data_down'],
         context['narratives_down']) = is_data_not_updated(res_json)
        context['technical_issues'] = flag_enabled('CCDB_TECHNICAL_ISSUES')
        return context


def get_narratives_json():
    """
    Main handler to deliver sample narratives to the landing page.
    """

    complaint_source = getattr(settings, 'COMPLAINT_LANDING_STATS_SOURCE', None)

    if not complaint_source:
        return DEMO_JSON

    try:
        res_json = requests.get(complaint_source).json()
    except requests.exceptions.RequestException as e:
        print("get_narratives_json:requests.exceptions.RequestException")
        print("There is a problem with getting data from the URL")
        print(e)
        res_json = {}
    except ValueError as e:
        print("get_narratives_json:ValueError")
        print("The text from the response doesn't follow "
              "the correct format to be parse as json")
        print(e)
        res_json = {}
    return res_json


def get_stats(res_json):
    res_stat = {}
    try:
        res_stat = res_json['stats']
    except KeyError as e:
        print("get_stats:KeyError")
        print("There is problem accessing with the given key, "
              "which probably means the json has missing data")
        print(e)

    return res_stat


def get_now():
    return datetime.now()


def is_data_not_updated(res_json):
    data_down = flag_enabled('CCDB_TECHNICAL_ISSUES')
    narratives_down = False
    # show notification starting fifth business day data has not been updated
    # M-Th, data needs to have been updated 6 days ago; F-S, preceding Monday
    weekday = datetime.weekday(get_now())
    delta = weekday if weekday > 3 else 6
    four_business_days_ago = (get_now() -
                              timedelta(delta)).strftime("%Y-%m-%d")

    try:

        if res_json['stats']['last_updated'] < four_business_days_ago:
            data_down = True
        elif (res_json['stats']['last_updated_narratives'] <
                four_business_days_ago):
            narratives_down = True
    except KeyError as e:
        print("is_data_not_updated:KeyError")
        print("There is problem accessing with the given key, "
              "which probably means the json has missing data")
        print(e)

    return (data_down, narratives_down)
