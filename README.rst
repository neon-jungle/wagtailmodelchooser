=====================
Wagtail model chooser
=====================

A plugin for Wagtail that provides convenience methods for setting up chooser modals 
for arbitrary models.


Installing
==========

Install using pip::

    pip install wagtail-modelchooser

Then add it to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'wagtailmodelchooser',
        # ...
    ]

It works with Wagtail 4.0 and upwards.
For older versions of Wagtail check previous versions of the package.

Quick start
===========

To enable the chooser for your model, you must register the model.
For simple cases, decorate your model with ``@register_model_chooser``:

.. code:: python

    from django.db import models

    from wagtailmodelchooser import register_model_chooser


    @register_model_chooser
    class Author(models.Model):
        name = models.CharField(max_length=255)

        def __str__(self):
            # The ``str()`` of your model will be used in the chooser
            return self.name

You can then use either ``FieldPanel`` in an edit handler definition,
or ``ModelChooserBlock`` in a ``StreamField`` definition:

.. code:: python

    from wagtail.wagtailcore.blocks import RichTextBlock
    from wagtail.wagtailcore.fields import StreamField
    from wagtail.wagtailcore.models import Page
    from wagtail.wagtailadmin.edit_handlers import FieldPanel
    from wagtailmodelchooser.blocks import ModelChooserBlock

    class Book(Page):
        name = models.CharField(max_length=255)
        author = models.ForeignKey(Author)

        content_panels = [
            FieldPanel('name'),
            FieldPanel('author'),
        ]

    class ContentPage(Page):
        body = StreamField([
            ('text', RichTextBlock()),
            ('author', ModelChooserBlock('books.Author')),
        ])

        content_panels = [
            StreamFieldPanel('body'),
        ]



Customisation options
=====================

If you want to customize the content or behaviour of the model chooser modal you have several options. These are illustrated through some examples below.

If you wanted to add an additional filter field to the popup, you might do that as follows:

.. code:: python

    from django.db import models

    from wagtailmodelchooser import register_model_chooser, Chooser


    class City(models.Model):
        name = models.CharField(max_length=255)
        capital = models.BooleanField()

        def __str__(self):
            # The ``str()`` of your model will be used in the chooser
            return self.name

    @register_model_chooser
    class CityChooser(Chooser):
        model = City
        modal_template = 'app_name/city_modal.html'
        modal_results_template = 'app_name/city_modal_results.html'

        def get_queryset(self, request):
            qs = super().get_queryset(request)
            if request.GET.get('capital'):
                qs = qs.filter(capital=request.GET.get('capital') == '0')

            return qs


Since wagtailmodelchooser is built largely on the (ChooserViewSet)[https://docs.wagtail.org/en/stable/extending/generic_views.html#chooserviewset] functionality already found in Wagtail, if you wish to do deeper customisation it is recommended to use that feature directly.
