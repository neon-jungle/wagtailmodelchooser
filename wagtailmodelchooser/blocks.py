from django.apps import apps

from . import registry
from .viewsets import viewset_factory


class ModelChooserBlock:
    def __new__(self, target_model, *args, **kwargs) -> None:
        if isinstance(target_model, str):
            target_model = apps.get_model(target_model)
            app_path = target_model
        else:
            app_path = (
                target_model._meta.app_label + "." + target_model._meta.model_name
            )

        chooser = registry.choosers[target_model]
        viewset = viewset_factory(chooser)
        return viewset.get_block_class(module_path=app_path)(*args, **kwargs)
