import json

from jinja2 import Template
from mkdocs.plugins import BasePlugin


class Plugin(BasePlugin):
    def on_page_markdown(self, markdown, page, **kwargs):
        page_jinja_context = page.meta.get('jinja')

        if not page_jinja_context:
            return markdown

        with open(page_jinja_context) as f:
            context = json.loads(f.read())

        return Template(markdown).render(**context)
