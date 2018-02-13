from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.utils.decorators import cached_classmethod

try:
    from wagtail.admin.edit_handlers import BaseChooserPanel
except ImportError:  # fallback for Wagtail <2.0
    from wagtail.wagtailadmin.edit_handlers import BaseChooserPanel

from .widgets import AdminModelChooser

FILTERS = {}


class BaseModelChooserPanel(BaseChooserPanel):
    filter_name = None

    @classmethod
    def widget_overrides(cls):
        return {cls.field_name: AdminModelChooser(
            model=cls.target_model(), filter_name=cls.filter_name)}

    @cached_classmethod
    def target_model(cls):
        return cls.model._meta.get_field(cls.field_name).rel.model

    def render_as_field(self):
        instance_obj = self.get_chosen_item()
        return mark_safe(render_to_string(self.field_template, {
            'field': self.bound_field,
            'instance': instance_obj,
        }))


class ModelChooserPanel(object):
    def __init__(self, field_name, filter_name=None):
        self.field_name = field_name
        self.filter_name = filter_name
        if filter_name is not None:
            FILTERS[filter_name] = filter

    def bind_to_model(self, model):
        return type(str('_ModelChooserPanel'), (BaseModelChooserPanel,), {
            'model': model,
            'field_name': self.field_name,
            'filter_name': self.filter_name,
        })
