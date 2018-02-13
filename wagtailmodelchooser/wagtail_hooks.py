from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html

try:
    from wagtail.core import hooks
except ImportError:  # fallback for Wagtail <2.0
    from wagtail.wagtailcore import hooks

import wagtailmodelchooser.urls


@hooks.register('register_admin_urls')
def register_model_chooser_admin_urls():
    return wagtailmodelchooser.urls.urlpatterns


@hooks.register('insert_editor_js')
def editor_js():
    return format_html('<script src="{}"></script>',
                       static('wagtailmodelchooser/js/model_chooser.js'))
