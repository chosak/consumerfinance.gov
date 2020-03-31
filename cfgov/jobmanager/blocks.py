from wagtail.core import blocks

from jobmanager.models import JobListingPage
from v1.util.util import extended_strftime


class JobListingList(blocks.StructBlock):
    more_jobs_page = blocks.PageChooserBlock(
        help_text='Link to full list of jobs'
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        jobs = JobListingPage.objects.open()[:5]
        request = context.get('request')

        context.update({
            'jobs': [
                {
                    'title': job.title,
                    'close_date': job.close_date,
                    'url': job.get_url(request=request),
                } for job in jobs
            ],
            'more_jobs_url': value['more_jobs_page'].get_url(request=request),
        })

        return context

    class Meta:
        icon = 'list-ul'
        template = 'jobmanager/job_listing_list.html'


class JobListingTable(blocks.StaticBlock):
    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        jobs = JobListingPage.objects.open()
        request = context.get('request')

        context.update({
            'jobs': jobs.values('title', 'url', 'close_date', 'location'),
        })

        header = [['TITLE', 'GRADE', 'POSTING CLOSES', 'LOCATION']]
        data = [
            [
                '<a href="%s">%s</a>' % (
                    job.get_url(request=request),
                    job.title,
                ),
                ', '.join(map(str, job.grades.all())),
                extended_strftime(job.close_date, '%_m %_d, %Y'),
                job.location_str,
            ] for job in jobs
        ]

        return {
            'value': {
                'data': header + data,
                'empty_table_msg': context['no_jobs_message'],
                'first_row_is_table_header': True,
                'has_data': bool(data),
                'is_stacked': True,
            },
        }

    def get_job_listings(self):
        return super().get_job_listings() \
            .prefetch_related('offices') \
            .prefetch_related('regions') \
            .prefetch_related('grades__grade')

    class Meta:
        icon = 'table'
        template = '_includes/organisms/table.html'
