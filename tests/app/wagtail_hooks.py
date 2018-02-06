from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Author


@modeladmin_register
class AuthorModelAdmin(ModelAdmin):
    model = Author
