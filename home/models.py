from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, MultipleChooserPanel
from modelcluster.fields import ParentalKey
from modelcluster.fields import ParentalManyToManyField
from django import forms
from wagtail.api import APIField
from wagtail.images.models import Image
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

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
    subtitle = models.CharField(max_length=255, blank=False, null=True)

    categories = ParentalManyToManyField(Category, blank=True)

    cover = models.ForeignKey(
        'wagtailimages.Image', verbose_name="Capa",
        null=True, blank=True, on_delete=models.SET_NULL)
    
    url_video = models.CharField(verbose_name="Video", max_length=255, blank=True, null=True)

    @property
    def has_video(self):
        return self.url_video is not None and self.url_video != ''

    api_fields = [
        APIField('body'),
        APIField('categories'),
    ]

    promote_panels = [
        FieldPanel('cover'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('body'),
        # FieldPanel('cover'),
        FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
    ]

    def save(self, *args, **kwargs):
        cache.clear()
        return super().save(*args, **kwargs)
