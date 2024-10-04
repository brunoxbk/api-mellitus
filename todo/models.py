from django.db import models
from django.utils import timezone
from django_currentuser.db.models import CurrentUserField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    user = CurrentUserField("Usuário", verbose_name="Usuário")

    panels = [
        FieldPanel("title"),
        FieldPanel("status"),
        FieldPanel("due_date"),
        FieldPanel("created_at", read_only=True),
    ]

    def __str__(self):
        return self.title

    def is_overdue(self):
        return self.due_date and timezone.now() > self.due_date and self.status != 'completed'
