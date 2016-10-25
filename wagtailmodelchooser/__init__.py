class Registry(object):
    def __init__(self):
        self.choosers = {}
        self.filters = {}

    def register_chooser(self, chooser):
        """Adds a model chooser definition to the registry."""
        self.choosers[chooser.model] = chooser()
        return chooser

    def register_simple_chooser(self, model, **kwargs):
        name = '{}Chooser'.format(model._meta.model_name)
        attrs = {'model': model}
        attrs.update(kwargs)

        chooser = type(name, (Chooser,), attrs)
        self.register_chooser(chooser)

        return model

    def register_filter(self, model, name, filter):
        assert model in self.choosers
        self.filters[(model, name)] = filter


class Chooser(object):
    model = None
    menu_icon = 'placeholder'

    def get_queryset(self, request):
        return self.model._default_manager.all()


registry = Registry()
register_model_chooser = registry.register_chooser
register_simple_model_chooser = registry.register_simple_chooser
register_filter = registry.register_filter
