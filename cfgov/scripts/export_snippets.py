import csv

from v1.models import Contact


def run():
    rows = []
    max_infos = 0

    for contact in Contact.objects.order_by('pk'):
        row = [
            contact.pk,
            contact.heading,
            contact.body,
        ]

        infos = contact.contact_info.stream_data
        max_infos = max(max_infos, len(infos))

        for info in infos:
            row.extend([
                info['type'],
                info['value'],
            ])

        rows.append(row)

    header = ['id', 'heading', 'body']
    for i in range(max_infos):
        header.extend([
            'contact %d' % i,
            'contact %d' % i,
        ])

    with open('snippets.csv', 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(header)

        for row in rows:
            writer.writerow(row)
