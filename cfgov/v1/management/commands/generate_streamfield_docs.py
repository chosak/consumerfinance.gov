from collections import OrderedDict as od
import json

from django.core.management.base import BaseCommand
from django.db import models

from collections import OrderedDict, defaultdict

from django.apps import apps
from wagtail.wagtailcore.blocks import StreamBlock
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page


class Command(BaseCommand):
    help = 'Generate Wagtail StreamField block documentation data'

    def handle(self, *args, **options):
        data = od([(
            '__notice__',
            'This file was automatically generated by {}.'.format(__name__),
        )])

        blocks, models = get_blocks_and_models()

        data.update(od([
            ('blocks', blocks),
            ('models', models),
        ]))

        self.stdout.write(json.dumps(data, indent=4))


def get_blocks_and_models():
    """Collect StreamField blocks and models with StreamFields."""
    blocks = defaultdict(dict)
    models = []

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
                if not isinstance(field, StreamField):
                    continue

                field_name = '.'.join([
                    model.__module__,
                    model.__name__,
                    field.name,
                ])

                stream_block = field.stream_block
                if not isinstance(stream_block, StreamBlock):
                    child_blocks = [stream_block]
                else:
                    child_blocks = list(stream_block.child_blocks.values())

                field_blocks = []
                for block in child_blocks:
                    block_name = block.__class__.__name__
                    block_fullname = '.'.join([
                        block.__class__.__module__,
                        block_name,
                    ])

                    block_data = blocks.setdefault(block_name, od([
                        ('name', block_name),
                        ('fullname', block_fullname),
                        ('module', block.__module__),
                        ('docstring', block.__doc__),
                        ('template', getattr(block.meta, 'template', None)),
                        ('fields', []),
                    ]))

                    block_data['fields'].append(field_name)

                    field_blocks.append(block_fullname)

                field_data = od([
                    ('name', field_name),
                    ('required', not field.blank),
                    ('blocks', field_blocks),
                ])

                streamfields.append(field_data)

            if streamfields:
                models.append(od([
                    ('name', model.__name__),
                    ('fullname', model.__module__ + '.' + model.__name__),
                    ('docstring', model.__doc__),
                    ('ispage', issubclass(model, Page)),
                    ('streamfields', streamfields),
                ]))

    return list(blocks.values()), models
