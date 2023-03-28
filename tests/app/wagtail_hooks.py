from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core.hooks import register

from .models import Author


@modeladmin_register
class AuthorModelAdmin(ModelAdmin):
    model = Author


@register("remove_bad_books")
def remove_bad_books(queryset, request):
    return queryset.filter(title__startswith="BAD")
