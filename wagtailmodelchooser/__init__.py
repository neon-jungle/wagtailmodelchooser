from .utils import kwarg_decorator, last_arg_decorator
from .version import version as __version__
from .version import version_info

__all__ = [
    "__version__",
    "version_info",
    "registry",
    "register_model_chooser",
    "register_simple_model_chooser",
    "register_filter",
    "Chooser",
]


class Registry(object):
    def __init__(self):
        self.choosers = {}
        self.filters = {}

    def register_chooser(self, chooser, **kwargs):
        """Adds a model chooser definition to the registry."""
        if not issubclass(chooser, Chooser):
            return self.register_simple_chooser(chooser, **kwargs)

        self.choosers[chooser.model] = chooser(**kwargs)
        return chooser

    def register_simple_chooser(self, model, **kwargs):
        """
        Generates a model chooser definition from a model, and adds it to the
        registry.
        """
        name = "{}Chooser".format(model._meta.object_name)
        attrs = {"model": model}
        attrs.update(kwargs)

        chooser = type(name, (Chooser,), attrs)
        self.register_chooser(chooser)

        return model

    def register_filter(self, model, name, filter):
        """Not currently used or documented, but could be re-implemented pretty easily"""
        assert model in self.choosers
        self.filters[(model, name)] = filter
        return filter


class Chooser(object):
    model = None
    icon = "placeholder"

    # Customize the chooser content for just this model
    modal_template = None
    modal_results_template = None

    def get_queryset(self, request):
        return self.model._default_manager.all()

    def get_modal_template(self, request):
        return self.modal_template or "wagtailadmin/generic/chooser/chooser.html"

    def get_modal_results_template(self, request):
        return (
            self.modal_results_template or "wagtailadmin/generic/chooser/results.html"
        )


registry = Registry()

register_model_chooser = kwarg_decorator(registry.register_chooser)
register_simple_model_chooser = kwarg_decorator(registry.register_simple_chooser)
register_filter = last_arg_decorator(registry.register_filter)
