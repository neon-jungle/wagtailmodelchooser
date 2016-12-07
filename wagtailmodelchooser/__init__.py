from .utils import kwarg_decorator, last_arg_decorator


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
        name = '{}Chooser'.format(model._meta.object_name)
        attrs = {'model': model}
        attrs.update(kwargs)

        chooser = type(name, (Chooser,), attrs)
        self.register_chooser(chooser)

        return model

    def register_filter(self, model, name, filter):
        assert model in self.choosers
        self.filters[(model, name)] = filter
        return filter


class Chooser(object):
    model = None
    icon = 'placeholder'

    def get_queryset(self, request):
        return self.model._default_manager.all()


registry = Registry()

register_model_chooser = kwarg_decorator(registry.register_chooser)
register_simple_model_chooser = kwarg_decorator(registry.register_simple_chooser)
register_filter = last_arg_decorator(registry.register_filter)
