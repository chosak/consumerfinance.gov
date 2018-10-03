import re


LARGER_HEADING_CLUSTERS = [
    {
        'cluster_id': 18,
        'answer_ids': [
            103,
            160,
            187,
            337,
            731,
            767,
            951,
            1157,
            1161,
            1403,
            1405,
            1439,
            1447,
            1567,
            1695,
        ],
    },
    {
        'cluster_id': 34,
        'answer_ids': [
            104,
            105,
            130,
            205,
            747,
            841,
            1423,
            1791,
        ],
    },
    {
        'cluster_id': 38,
        'answer_ids': [
            143,
            184,
            329,
            331,
            1165,
            1637,
            1787,
            1789,
            1797,
            1921,
            1923,
        ],
    },
    {
        'cluster_id': 49,
        'answer_ids': [
            136,
            161,
            163,
            164,
            172,
            176,
            179,
            180,
            181,
            188,
            192,
            336,
            817,
            1699,
            1983,
            1989,
            1995,
            1997,
            2001,
        ],
    },
    {
        'cluster_id': 93,
        'answer_ids': [
            146,
            226,
            237,
            318,
            338,
            545,
            633,
            811,
            1215,
            1463,
            1507,
        ],
    },
]


def _get_answer_id_from_request(request):
    """Given a Django request, return the Answer ID.

    Returns None if no Answer ID could be determined from the request.

    This is something of a hack because it hardcodes the expected path to Ask
    pages and their URL format. It would be better if instead we had the Page
    object itself from which we could grab the answer ID.
    """
    match = re.match(r'^/ask-cfpb/.+-(\d+)/$', request.path)

    if match:
        return int(match.group(1))


def larger_heading(request):
    answer_id = _get_answer_id_from_request(request)

    if answer_id:
        return any(
            answer_id in cluster['answer_ids']
            for cluster in LARGER_HEADING_CLUSTERS
        )
