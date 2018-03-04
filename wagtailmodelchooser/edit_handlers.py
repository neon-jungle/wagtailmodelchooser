from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.admin.edit_handlers import BaseChooserPanel

from .widgets import AdminModelChooser

FILTERS = {}


class ModelChooserPanel(BaseChooserPanel):
    model = None
    field_name = None
    filter_name = None

    def __init__(self, field_name, filter_name=None, **kwargs):
        super().__init__(field_name, **kwargs)

        self.filter_name = filter_name
        if filter_name is not None:
            FILTERS[filter_name] = filter

    def widget_overrides(self):
        return {self.field_name: AdminModelChooser(
            model=self.target_model, filter_name=self.filter_name)}

    @property
    def target_model(self):
        return self.model._meta.get_field(self.field_name).remote_field.model

    def render_as_field(self):
        instance_obj = self.get_chosen_item()
        return mark_safe(render_to_string(self.field_template, {
            'field': self.bound_field,
            'instance': instance_obj,
        }))
