import re

from django.conf import settings
from django.utils.module_loading import import_string

from flags import conditions


def _get_deploy_environment():
    return getattr(settings, 'DEPLOY_ENVIRONMENT', None)


@conditions.register('environment is')
def environment_is(environment, **kwargs):
    return environment == _get_deploy_environment()


@conditions.register('environment is not')
def environment_is_not(environment, **kwargs):
    return environment != _get_deploy_environment()


@conditions.register('experiment')
def experiment(experiment_fn_path, request, **kwargs):
    experiment_fn = import_string(experiment_fn_path)
    return experiment_fn(request)
