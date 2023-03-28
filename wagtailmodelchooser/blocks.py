from django.utils.functional import cached_property, lazy
from wagtail.coreutils import resolve_model_string

from . import registry
from .viewsets import DeconstructibleChooserBlock, viewset_factory


class ModelChooserBlock(DeconstructibleChooserBlock):
    def __init__(self, target_model, filter_name=None, **kwargs):
        super(ModelChooserBlock, self).__init__(**kwargs)
        self._target_model = target_model

        self.filter_name = filter_name

        if self.meta.icon == "placeholder":
            # Get the icon from the chooser.
            # The chooser may not have been registered yet, depending upon
            # import orders and things, so get the icon lazily
            self.meta.icon = lazy(lambda: self.chooser.icon, str)()

    @cached_property
    def target_model(self):
        return resolve_model_string(self._target_model)

    @cached_property
    def viewset(self):
        return viewset_factory(self.chooser)

    @cached_property
    def widget(self):
        return self.viewset.widget_class()

    @cached_property
    def chooser(self):
        return registry.choosers[self.target_model]

    def get_form_state(self, value):
        return self.widget.get_value_data(value)

    class Meta:
        icon = "placeholder"
