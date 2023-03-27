from wagtail import hooks

from . import registry
from .viewsets import viewset_factory


@hooks.register("register_admin_viewset")
def register_model_viewsets():
    viewsets = []
    for chooser in registry.choosers.values():
        viewsets.append(viewset_factory(chooser))
    return viewsets
