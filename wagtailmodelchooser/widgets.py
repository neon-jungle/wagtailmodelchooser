import json

from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.widgets import AdminChooser

try:
    from wagtail.core.telepath import register
    from wagtail.core.widget_adapters import WidgetAdapter
except ImportError:  # do-nothing fallback for Wagtail <2.13
    def register(adapter, cls):
        pass

    class WidgetAdapter:
        pass


class AdminModelChooser(AdminChooser):
    show_edit_link = False

    def __init__(self, model, filter_name=None, **kwargs):
        self.target_model = model
        name = self.target_model._meta.verbose_name
        self.choose_one_text = _('Choose %s') % name
        self.choose_another_text = _('Choose another %s') % name
        self.link_to_chosen_text = _('Edit this %s') % name

        self.filter_name = filter_name

        super(AdminModelChooser, self).__init__(**kwargs)

    def get_value_data(self, value):
        # return a dict of data required for rendering a widget with this value -
        # namely, the ID and string representation
        if value is None:
            return None
        elif isinstance(value, self.target_model):
            instance = value
        else:  # assume this is an instance ID
            instance = self.target_model.objects.get(pk=value)

        return {
            'id': instance.pk,
            'display_title': str(instance),
        }

    def render_html(self, name, value, attrs):
        if WAGTAIL_VERSION >= (2, 13):
            # From Wagtail 2.13, get_value_data is called as a preprocessing step in
            # WidgetWithScript before invoking render_html
            value_data = value or {}
        else:
            value_data = self.get_value_data(value) or {}

        original_field_html = super(AdminModelChooser, self).render_html(
            name, value_data.get('id'), attrs)

        return render_to_string("wagtailmodelchooser/model_chooser.html", {
            'widget': self,
            'model_opts': self.target_model._meta,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': bool(value_data),  # only used to identify blank values
            'display_title': value_data.get('display_title', ''),
        })

    @property
    def modal_url(self):
        opts = self.target_model._meta
        kwargs = {'app_label': opts.app_label, 'model_name': opts.model_name}
        if self.filter_name:
            kwargs['filter_name'] = self.filter_name

        return reverse('model_chooser', kwargs=kwargs)

    def render_js_init(self, id_, name, value):
        return "wagtail.ui.ModelChooser.setupWagtailWidget({id}, {url});".format(
            id=json.dumps(id_),
            url=json.dumps(self.modal_url))


class ModelChooserAdapter(WidgetAdapter):
    js_constructor = 'wagtailmodelchooser.widgets.ModelChooser'

    def js_args(self, widget):
        return [
            widget.render_html('__NAME__', None, attrs={'id': '__ID__'}),
            widget.modal_url,
        ]

    class Media:
        js = [
            'wagtailmodelchooser/js/model_chooser_telepath.js',
        ]


register(ModelChooserAdapter(), AdminModelChooser)
