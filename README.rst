=====================
Wagtail model chooser
=====================

A plugin for Wagtail that provides a ``ModelChooserPanel`` and ``ModelChooserBlock``
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

It works with Wagtail 1.4 and upwards.

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

You can then use either ``ModelChooserPanel`` in an edit handler definition,
or ``ModelChooserBlock`` in a ``StreamField`` definition:

.. code:: python

    from wagtail.wagtailcore.blocks import RichTextBlock
    from wagtail.wagtailcore.fields import StreamField
    from wagtail.wagtailcore.models import Page
    from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel
    from wagtailmodelchooser.blocks import ModelChooserBlock
    from wagtailmodelchooser.edit_handlers import ModelChooserPanel

    class Book(Page):
        name = models.CharField(max_length=255)
        author = models.ForeignKey(Author)

        content_panels = [
            FieldPanel('name'),
            ModelChooserPanel('author'),
        ]

    class ContentPage(Page):
        body = StreamField([
            ('text', RichTextBlock()),
            ('author', ModelChooserBlock('books.Author')),
        ])

        content_panels = [
            StreamFieldPanel('body'),
        ]
