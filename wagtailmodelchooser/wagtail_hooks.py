from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html
from wagtail.core import hooks

import wagtailmodelchooser.urls


@hooks.register('register_admin_urls')
def register_model_chooser_admin_urls():
    return wagtailmodelchooser.urls.urlpatterns


@hooks.register('insert_editor_js')
def editor_js():
    return format_html('<script src="{}"></script>',
                       static('wagtailmodelchooser/js/model_chooser.js'))
