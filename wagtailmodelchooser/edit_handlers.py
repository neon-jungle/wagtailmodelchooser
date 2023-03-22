from django.utils.functional import cached_property
from wagtail.admin.panels import FieldPanel

from .widgets import AdminModelChooser

FILTERS = {}


class ModelChooserPanel(FieldPanel):
    model = None
    field_name = None
    filter_name = None

    def __init__(self, field_name, filter_name=None, **kwargs):
        super().__init__(field_name, **kwargs)

        self.filter_name = filter_name
        if filter_name is not None:
            FILTERS[filter_name] = filter

    def clone(self):
        return self.__class__(
            field_name=self.field_name,
            filter_name=self.filter_name,
            widget=self.widget if hasattr(self, 'widget') else None,
            heading=self.heading,
            classname=self.classname,
            help_text=self.help_text
        )

    def get_form_options(self):
        opts = super().get_form_options()

        widgets = opts.setdefault("widgets", {})
        widgets[self.field_name] = AdminModelChooser(
            model=self.target_model, filter_name=self.filter_name)

        return opts

    @property
    def target_model(self):
        return self.model._meta.get_field(self.field_name).remote_field.model

    @cached_property
    def widget(self):

        return AdminModelChooser(
            model=self.target_model, filter_name=self.filter_name)
