from django.db import models
from django_currentuser.db.models import CurrentUserField
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet


@register_snippet
class GlycemiaLog(ClusterableModel):
    value = models.FloatField("Valor")
    measurement_time = models.DateTimeField("Horário", auto_now_add=True)
    notes = models.TextField("Observações", null=True, blank=True)
    user = CurrentUserField("Usuário", verbose_name="Usuário")

    def __str__(self):
        return (
            f"{self.value} mg/dL em {self.measurement_time.strftime('%Y-%m-%d %H:%M')}"
        )

    # panels = [
    #     FieldPanel("value"),
    #     FieldPanel("measurement_time"),
    #     InlinePanel("notes"),
    #     InlinePanel("user "),
    # ]

    class Meta:
        db_table = "glycemia_log"
        verbose_name = "Medição de Glicemia"
        verbose_name_plural = "Medições de Glicemia"
        ordering = ["-measurement_time"]
