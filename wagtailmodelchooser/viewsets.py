from wagtail.admin.viewsets.chooser import ChooserViewSet


def viewset_factory(chooser):
    name = chooser.model._meta.model_name
    return type(
        f"{name.capitalize()}ChooserViewSet",
        (ChooserViewSet,),
        {"model": chooser.model, "icon": chooser.icon},
    )(f"{name}_chooser")
