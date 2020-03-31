from datetime import date


job_defaults = {
    'title': 'Director, Example Division',
    'offices': ['Washington, DC'],
    'regions': [],
    'close_date': date(2099, 1, 1),
    'division': 'Operations',
    'grades': [30],
    'salary_min': 50000,
    'salary_max': 100000,
    'applicant_types': [
        'Open to All US Citizens (Competitive service - Permanent)',
    ],
}


job_listing_details_test_cases = {
    'Job in single office': {},

    'Job in single office, remote allowed': {'remote_allowed': True},

    'Job with two offices': {'offices': ['Washington, DC', 'New York, NY']},

    'Job with two offices, remote allowed': {
        'offices': ['Washington, DC', 'New York, NY'],
        'remote_allowed': True,
    },

    'Job with three offices': {
        'offices': ['Washington, DC', 'New York, NY', 'Atlanta, GA'],
    },

    'Job with three offices, remote allowed': {
        'offices': ['Washington, DC', 'New York, NY', 'Atlanta, GA'],
        'remote_allowed': True,
    },

    'Job for a single region': {
        'regions': [
            {
                'name': 'Northeast',
                'states': ['AB', 'CD', 'EF', 'GH', 'IJ'],
                'major_cities': ['Washington, DC', 'New York, NY'],
            },
        ],
    },

    'Job for two regions': {
        'regions': [
            {
                'name': 'Northeast',
                'states': ['AB', 'CD', 'EF', 'GH', 'IJ'],
                'major_cities': ['Washington, DC', 'New York, NY'],
            },
            {
                'name': 'Southwest',
                'states': ['AB', 'CD', 'EF', 'GH', 'IJ'],
                'major_cities': ['Phoenix, AZ', 'Las Vegas, NV'],
            },
        ],
    },

    'Job for four regions': {
        'regions': [
            {
                'name': 'Northeast',
                'states': ['AB', 'CD', 'EF', 'GH', 'IJ'],
                'major_cities': ['Washington, DC', 'New York, NY'],
            },
            {
                'name': 'Southeast',
                'states': ['AB', 'CD', 'EF', 'GH', 'IJ'],
                'major_cities': ['Atlanta, GA', 'Baltimore, MD'],
            },
            {
                'name': 'Southwest',
                'states': ['AB', 'CD', 'EF', 'GH', 'IJ'],
                'major_cities': ['Phoenix, AZ', 'Las Vegas, NV'],
            },
            {
                'name': 'Midwest',
                'states': ['AB', 'CD', 'EF', 'GH', 'IJ'],
                'major_cities': ['Chicago, IL', 'St. Louis, MO'],
            },
        ],
    },

    'Job with no location': {'offices': [], 'regions': []},

    'Job with single grade': {},

    'Job with multiple grades': {'grades': [52, 53, 60]},

    'Job with no grades': {'grades': []},

    'Job with month that should not get abbreviated': {
        'close_date': date(2099, 6, 1),
    },

    'Job with single applicant type': {},

    'Job with multiple applicant types': {
        'applicant_types': [
            'Open to All US Citizens (Competitive service - Permanent)',
            'Open to status candidates (Competitive service - Permanent)',
        ],
    },

    'Job with no applicant types': {'applicant_types': []},
}


for job in job_listing_details_test_cases.values():
    for k, v in job_defaults.items():
        job.setdefault(k, v)


job_listing_list_test_cases = {
    'No open jobs': {},

    'Single open job': {
        'jobs': [
            {
                'title': 'Director, Example Division',
                'url': '/jobs/example/',
                'close_date': date(2099, 1, 1),
            },
        ],
    },

    'Multiple open jobs': {
        'jobs': [
            {
                'title': f'Open job {i}',
                'url': f'/jobs/{i}',
                'close_date': date(2099, i, 1),
            } for i in range(5, 0, -1)
        ],
    },
}


job_listing_table_test_cases = {
    'No open jobs': {},

    'Single open job': {
        'jobs': [
            {
                'title': 'Example job',
                'url': '/jobs/example/',
                'grades': [30],
                'close_date': date(2099, 1, 1),
                'regions': [],
                'offices': ['Washington, DC'],
            },
        ],
    },

    'Multiple open jobs': {
        'jobs': [
            dict(job, title=title)
            for title, job in job_listing_details_test_cases.items()
        ],
    },
}
