import json

from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.widgets import BaseChooser
from wagtail.images.shortcuts import get_rendition_or_not_found

if WAGTAIL_VERSION[0] >= 3:
    from wagtail.telepath import register
    from wagtail.widget_adapters import WidgetAdapter
elif WAGTAIL_VERSION[:2] >= (2, 13):
    from wagtail.core.telepath import register
    from wagtail.core.widget_adapters import WidgetAdapter
else:
    # do-nothing fallback for Wagtail <2.13
    def register(adapter, cls):
        pass

    class WidgetAdapter:
        pass


class AdminModelChooser(BaseChooser):
    show_edit_link = False
    js_constructor_name = "ModelChooser"

    def __init__(self, model, filter_name=None, **kwargs):
        self.target_model = model
        self.model_class = model
        name = self.target_model._meta.verbose_name
        self.icon = "snippet"
        self.choose_one_text = _('Choose %s') % name
        self.choose_another_text = _('Choose another %s') % name
        self.link_to_chosen_text = _('Edit this %s') % name
        self.chooser_modal_url_name = "model_chooser"
        self.template_name = "wagtailmodelchooser/model_chooser.html"

        self.filter_name = filter_name

        super(AdminModelChooser, self).__init__(**kwargs)

    def get_value_data_from_instance(self, instance):
        data = super().get_value_data_from_instance(instance)
        if hasattr(instance, "model_chooser_icon") and instance.model_chooser_icon:
            preview_image = get_rendition_or_not_found(instance.model_chooser_icon, "max-165x165")
            data["preview"] = {
                "url": preview_image.url,
                "width": preview_image.width,
                "height": preview_image.height,
            }
        return data

    def get_context(self, name, value_data, attrs):
        context = super().get_context(name, value_data, attrs)
        context["preview"] = value_data.get("preview", {})
        return context

    def get_chooser_modal_url(self):
        return self.modal_url

    @property
    def modal_url(self):
        opts = self.target_model._meta
        kwargs = {'app_label': opts.app_label, 'model_name': opts.model_name}
        if self.filter_name:
            kwargs['filter_name'] = self.filter_name

        return reverse('model_chooser', kwargs=kwargs)

    def js_opts(self):
        return self.get_chooser_modal_url()

    def render_js_init(self, id_, name, value):
        opts = self.js_opts()
        if opts:
            return "new {constructor}({id}, {opts});".format(
                constructor=self.js_constructor_name, id=json.dumps(id_), opts=json.dumps(opts)
            )
        else:
            return "new {constructor}({id});".format(
                constructor=self.js_constructor_name, id=json.dumps(id_)
            )


class ModelChooserAdapter(WidgetAdapter):
    js_constructor = 'wagtailmodelchooser.widgets.ModelChooser'

    def js_args(self, widget):
        return [
            widget.render_html('__NAME__', None, attrs={'id': '__ID__'}),
            widget.modal_url,
        ]

    class Media:
        js = [
            'wagtailmodelchooser/js/model_chooser.js',
            'wagtailmodelchooser/js/model_chooser_telepath.js',
        ]


register(ModelChooserAdapter(), AdminModelChooser)
