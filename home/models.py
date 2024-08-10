from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, MultipleChooserPanel
from modelcluster.fields import ParentalKey
from modelcluster.fields import ParentalManyToManyField
from django import forms
from wagtail.api import APIField

class HomePage(Page):
    pass


@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class PostPage(Page):
    body = RichTextField(blank=True)

    categories = ParentalManyToManyField(Category, blank=True)

    api_fields = [
        APIField('body'),
        APIField('categories'),
    ]


    content_panels = Page.content_panels + [
        FieldPanel('body'),
        FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
    ]
