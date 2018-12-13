from setuptools import setup


setup(
    name='mkdocs-jinja-plugin',
    install_requires=['Jinja2'],
    py_modules=['mkdocs_jinja'],
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-jinja = mkdocs_jinja:Plugin',
        ]
    }
)
