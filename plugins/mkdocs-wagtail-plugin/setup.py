from setuptools import setup


setup(
    name='mkdocs-wagtail-plugin',
    packages=['mkdocs_wagtail'],
    entry_points={
        'mkdocs.plugins': [
            'mkdocs_wagtail = mkdocs_wagtail.plugin:Plugin',
        ]
    }
)
