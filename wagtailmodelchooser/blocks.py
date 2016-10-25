from django.utils.functional import cached_property
from wagtail.wagtailcore.blocks import ChooserBlock
from wagtail.wagtailcore.utils import resolve_model_string

from .widgets import AdminModelChooser


class ModelChooserBlock(ChooserBlock):
    def __init__(self, target_model, *, filter=None, **kwargs):
        super().__init__(**kwargs)
        self._target_model = target_model
        self.filter_name = filter

    @cached_property
    def target_model(self):
        return resolve_model_string(self._target_model)

    @cached_property
    def widget(self):
        return AdminModelChooser(self.target_model,
                                 filter_name=self.filter_name)

    def deconstruct(self):
        name, args, kwargs = super().deconstruct()

        if args:
            args = args[1:]  # Remove the args target_model

        kwargs['target_model'] = self.target_model._meta.label_lower
        return name, args, kwargs

    class Meta:
        icon = "placeholder"
