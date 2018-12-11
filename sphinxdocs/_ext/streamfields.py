from docutils import nodes
from django.apps import apps

from sphinx import addnodes
from sphinx.util.docutils import SphinxDirective

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page


def get_model_streamfields():
    model_streamfields = {}

    for app_config in apps.get_app_configs():
        if app_config.name.startswith('wagtail'):
            continue

        for model in app_config.get_models():
            streamfields = []

            if model._meta.abstract:
                continue

            if issubclass(model, Page) and not model.is_creatable:
                continue

            for field in model._meta.fields:
                if isinstance(field, StreamField):
                    streamfields.append(field)

            if streamfields:
                model_streamfields[model] = streamfields

    return model_streamfields


def find_streamfield_blocks(app):
    env = app.builder.env
    env.model_streamfields = get_model_streamfields()


def noop(self, node):
    pass


class streamfield_block_modules_toc(nodes.comment):
    pass

def streamfield_block_modules_toc_visit_html(self, node):
    raise nodes.SkipNode


class StreamFieldBlockModules(SphinxDirective):
    def run(self):
        model_streamfields = self.env.model_streamfields
	nodes = []

        docnames = ['blocks/foo', 'blocks/bar']

	tocnode = addnodes.toctree()
	tocnode['includefiles'] = docnames
	tocnode['entries'] = [(None, docn) for docn in docnames]
	tocnode['maxdepth'] = -1
	tocnode['glob'] = None

	nodes.append(streamfield_block_modules_toc('', '', tocnode))

	return nodes



def setup(app):
    app.connect('builder-inited', find_streamfield_blocks)
    app.add_node(
        streamfield_block_modules_toc,
        html=(streamfield_block_modules_toc_visit_html, noop)
    )
    app.add_directive('streamfield_block_modules', StreamFieldBlockModules)
    return {'parallel_read_safe': True}
