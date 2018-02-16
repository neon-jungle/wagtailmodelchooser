import re

from django.apps import apps
from django.http import Http404
from django.shortcuts import render
from wagtail.utils.pagination import paginate

try:
    from wagtail.admin.modal_workflow import render_modal_workflow
    from wagtail.search.index import Indexed
except ImportError:  # fallback for Wagtail <2.0
    from wagtail.wagtailadmin.modal_workflow import render_modal_workflow
    from wagtail.wagtailsearch.index import Indexed

from . import registry

instance_str_re = re.compile(r'^([a-z0-9_]+\.[a-zA-Z0-9]+):(.*)$')


def instance_from_str(instance_str):
    """
    Given an instance string in the form "app.Model:pk", returns a tuple of
    ``(model, instance)``. If the pk part is empty, ``instance`` will be
    ``None``. Raises ``ValueError`` on invalid model strings or missing
    instances.
    """
    match = instance_str_re.match(instance_str)
    if not match:
        raise ValueError("Invalid instance string")

    model_string = match.group(1)
    try:
        model = apps.get_model(model_string)
    except (LookupError, ValueError):
        raise ValueError("Invalid instance string")

    pk = match.group(2)
    if pk:
        try:
            return model, model._default_manager.get(pk=pk)
        except model.DoesNotExist:
            raise ValueError("Invalid instance string")

    return model, None


def chooser(request, app_label, model_name, filter_name=None):

    try:
        model = apps.get_model(app_label, model_name)
        chooser = registry.choosers[model]
    except (LookupError, ValueError, KeyError):
        raise Http404

    qs = chooser.get_queryset(request)

    is_searchable = issubclass(model, Indexed)
    is_searching = is_searchable and request.GET.get('q')

    if is_searching:
        qs = qs.search(request.GET['q'])

    if filter_name is not None:
        try:
            filter_func = registry.filters[model, filter_name]
        except KeyError:
            raise Http404
        qs = filter_func(qs)

    paginator, page = paginate(request, qs, per_page=10)
    ajax = 'ajax' in request.GET

    context = {
        'chooser': chooser,
        'chooser_url': request.path,
        'opts': model._meta,
        'paginator': paginator,
        'page': page,
        'object_list': page.object_list,
        'is_searchable': is_searchable,
        'is_searching': is_searching,
    }

    if ajax:
        return render(request, 'wagtailmodelchooser/results.html', context)
    else:
        return render_modal_workflow(
            request,
            'wagtailmodelchooser/modal.html',
            'wagtailmodelchooser/modal.js',
            context)
