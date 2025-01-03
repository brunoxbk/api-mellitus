from django.db import models
from django.utils import timezone
from django_currentuser.db.models import CurrentUserField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Medication(models.Model):
    FREQUENCY_CHOICES = (
        (1, "1x"),
        (2, "2x"),
        (3, "3x"),
        (4, "4x"),
    )
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.IntegerField(choices=FREQUENCY_CHOICES)
    time = models.TimeField()
    instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = CurrentUserField("Usuário", verbose_name="Usuário")

    panels = [
        FieldPanel("name"),
        FieldPanel("dosage"),
        FieldPanel("frequency"),
        FieldPanel("time"),
        FieldPanel("instructions"),
        FieldPanel("created_at", read_only=True),
    ]

    class Meta:
        verbose_name = "Medicação"
        verbose_name_plural = "Medicações"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class MedicationLog(models.Model):
    medication = models.ForeignKey(
        Medication, on_delete=models.CASCADE, related_name="logs"
    )
    taken_at = models.DateTimeField()
    was_taken = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Medicação Log"
        verbose_name_plural = "Medicações Log"
        ordering = ["-taken_at"]

    def __str__(self):
        return f"{self.medication.name} - {self.taken_at.strftime('%d-%m-%Y %H:%M')}"
