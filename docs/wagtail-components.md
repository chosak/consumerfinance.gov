---
# This page documents the various StreamFields and StreamField blocks that
# exist within this project. Because these fields and blocks change
# frequently, and to avoid having to maintain this page every time they
# change, some of the content in this page is generated programmatically from
# the project source code.
#
# This file leverages the mkdocs-jinja plugin to load content from an
# external JSON file and render it using Jinja templating. The JSON file
# contains information about the project fields and blocks, inserted here via
# these variables:
#
# - `models`: Django models (including Wagtail Pages) containing StreamFields.
# - `blocks`: Available block types across all model StreamFields.
#
# The JSON file can be updated by capturing the output of this Django
# management command when run inside of a project Python environment:
#
# `cfgov/manage.py generate_streamfield_docs > docs/wagtail-components.json`
#
# The code that powers that management command lives here:
#
# `cfgov/v1/management/commands/generate_streamfield_docs.py`
#
# The following directive tells MkDocs to use the mkdocs-jinja plugin to
# enable Jinja templating for this file and to load the specified JSON file's
# contents into the Jinja template context.
jinja: docs/wagtail-components.json
---
# Wagtail components

## StreamField block types

{% for module, blocks in blocks|sort(attribute='module')|groupby('module') %}
### {{ module }}

{% for block in blocks %}
#### {{ block.name }}

- Module: `{{ block.fullname }}`
{% if block.template %}- Template: `{{ block.template }}`{% endif %}
{% if block.fields %}
- Available in:
    {% for field in block.fields|sort %}
    - `{{ field }}`
    {% endfor %}
{% endif %}

{% if block.docstring %}
{{ block.docstring }}
{% endif %}
{% endfor %}

{% endfor %}

{% macro showmodels(models) -%}
{% for model in models|sort(attribute='name') %}
#### {{ model.name }}

- Module: `{{ model.fullname }}`
- StreamFields:
    {% for field in model.streamfields %}
    - `{{ field.name }}`{% if field.required %} (required){% endif %}
    {% endfor %}

{% if model.docstring %}
{{ model.docstring }}
{% endif %}
{% endfor %}
{%- endmacro %}

## Wagtail Page types containing StreamFields
{{ showmodels(models|selectattr('ispage')) }}

## Django models containing StreamFields
{{ showmodels(models|rejectattr('ispage')) }}
