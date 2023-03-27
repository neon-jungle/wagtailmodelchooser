from functools import cached_property

from wagtail.admin.views.generic import chooser as chooser_views
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.blocks.field_block import ChooserBlock

from . import registry


class DeconstructibleChooserBlock(ChooserBlock):
    # only used in migrations, which are useless anyway for streamfields
    def deconstruct(self):
        return (
            "wagtailmodelchooser.blocks.ModelChooserBlock",
            (self.model_class,) + self._constructor_args[0],
            self._constructor_args[1],
        )


class ModelRegistryMixin:
    @property
    def template_name(self):
        return self.chooser.get_modal_template(self.request)

    @property
    def results_template_name(self):
        return self.chooser.get_modal_results_template(self.request)

    @cached_property
    def chooser(self):
        return registry.choosers[self.model_class]

    def get_object_list(self):
        return self.chooser.get_queryset(self.request)


class ModelChooseView(ModelRegistryMixin, chooser_views.ChooseView):
    pass


class ModelResultsView(ModelRegistryMixin, chooser_views.ChooseResultsView):
    pass


def viewset_factory(chooser):
    model_name = chooser.model.__name__
    nice_name = chooser.model._meta.verbose_name

    return type(
        f"{model_name}ChooserViewSet",
        (ChooserViewSet,),
        {
            "model": chooser.model,
            "icon": chooser.icon,
            "choose_one_text": f"Choose {nice_name}",
            "choose_another_text": f"Choose another {nice_name}",
            "link_to_chosen_text": f"Edit this {nice_name}",
            "choose_view_class": ModelChooseView,
            "choose_results_view_class": ModelResultsView,
            "base_block_class": DeconstructibleChooserBlock,
        },
    )(f"{model_name.lower()}_chooser")
