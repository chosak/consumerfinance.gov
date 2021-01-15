from django.utils.safestring import mark_safe


DESIGN_SYSTEM_ROOT = 'https://cfpb.github.com/design-system/'


def design_system_link(title, path):
    link_text = 'See documentation in the CFPB Design System'

    link = (
        '<a '
        f'href="{DESIGN_SYSTEM_ROOT}{path}" '
        'target="_blank" '
        'rel="noopener noreferrer"'
        '>'
        f'{link_text}'
        '</a>'
    )

    return mark_safe(f'{title} ({link})')
