from django.contrib.auth.models import User
from django.db import models
from django_currentuser.db.models import CurrentUserField
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet

# @register_snippet
# class Kind(models.Model):
#     text = models.CharField(max_length=255)
#     created_at = models.DateTimeField(
#         "Criado em", editable=False, auto_now_add=True)
#     updated_at = models.DateTimeField(
#         "Alterado em", editable=False, auto_now=True)

#     def __str__(self):
#         return self.text


@register_snippet
class Form(ClusterableModel):
    class TypeForm(models.TextChoices):
        OBJECTIVE = "1", "Objetiva"
        AGREEMENT = "2", "Concordância/Discordância"
        DICHOTOMOUS = "3", "Dicotômica"

    title = models.CharField("Título", max_length=255)
    description = models.TextField("Descrição", max_length=800)
    created_at = models.DateTimeField("Criado em", editable=False, auto_now_add=True)
    updated_at = models.DateTimeField("Alterado em", editable=False, auto_now=True)
    # kind = models.ForeignKey(Kind, related_name='forms_kind', on_delete=models.CASCADE)
    type_form = models.CharField(
        "Tipo de resposta", max_length=1, choices=TypeForm.choices
    )

    @property
    def is_objective(self):
        return self.type_form == self.TypeForm.OBJECTIVE

    @property
    def is_agrreement(self):
        return self.type_form == self.TypeForm.AGREEMENT
    
    @property
    def is_dichotomous(self):
        return self.type_form == self.TypeForm.DICHOTOMOUS

    @property
    def answered(self):
        return self.form_sheet_answers.all().exists()

    def score(self):
        answer = self.form_sheet_answers.last()

        if answer:
            if self.is_objective:
                return answer.score_knowledge
            elif self.is_agrreement:
                return answer.score_weight
            elif self.is_dichotomous:
                return answer.score_dicotomic
        
        return 0

    def score_text(self):
        answer = self.form_sheet_answers.last()
        if answer:
            if self.is_objective:
                return answer.score_knowledge_text
            elif self.is_agrreement:
                return answer.score_weight_text
            elif self.is_dichotomous:
                return answer.score_dicotomic_text
        
        return ""

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("type_form"),
        InlinePanel("questions"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        db_table = "forms"
        verbose_name = "Formulário"
        verbose_name_plural = "Formulários"
        ordering = ["-created_at"]


@register_snippet
class Question(ClusterableModel):
    text = models.TextField("Enunciado", max_length=800)
    form = ParentalKey(
        "instruments.Form", related_name="questions", verbose_name="Formulário"
    )
    created_at = models.DateTimeField("Criado em", editable=False, auto_now_add=True)
    updated_at = models.DateTimeField("Alterado em", editable=False, auto_now=True)

    panels = [
        FieldPanel("form"),
        FieldPanel("text"),
        InlinePanel("choices"),
    ]

    def __str__(self):
        return self.text

    class Meta:
        db_table = "question"
        verbose_name = "Questão"
        verbose_name_plural = "Questões"
        ordering = ["-created_at"]


class Choice(ClusterableModel):
    # question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    question = ParentalKey(
        "instruments.Question", related_name="choices", verbose_name="Questão"
    )
    text = models.CharField("Alternativa", max_length=255)
    is_correct = models.BooleanField("Correta", default=False)
    weight = models.FloatField("Peso", default=0.0)
    created_at = models.DateTimeField("Criado em", editable=False, auto_now_add=True)
    updated_at = models.DateTimeField("Alterado em", editable=False, auto_now=True)

    def __str__(self):
        return f"{self.text} (Correct: {self.is_correct}, Weight: {self.weight})"

    panels = [FieldPanel("text"), FieldPanel("is_correct"), FieldPanel("weight")]

    class Meta:
        db_table = "choices"
        verbose_name = "Alternativa"
        verbose_name_plural = "Alternativas"
        ordering = ["pk"]


@register_snippet
class AnswerSheet(models.Model):
    form = models.ForeignKey(
        Form, related_name="form_sheet_answers", on_delete=models.CASCADE
    )
    user = CurrentUserField("Usuário", verbose_name="Usuário")

    created_at = models.DateTimeField("Criado em", editable=False, auto_now_add=True)
    updated_at = models.DateTimeField("Alterado em", editable=False, auto_now=True)

    panels = [
        FieldPanel("form"),
        FieldPanel("user"),
        InlinePanel("sheet_answers"),
    ]

    @property
    def score_dicotomic(self):
        return self.sheet_answers.filter(choice__is_correct=True).count()

    @property
    def score_knowledge(self):
        return self.sheet_answers.filter(choice__is_correct=True).count()

    @property
    def score_weight(self):
        return self.sheet_answers.all().aggregate(models.Sum("choice__weight"))[
            "choice__weight__sum"
        ]

    @property
    def score_weight_text(self):
        if self.score_weight > 70:
            result = "Atitude positiva em relação à doença."
        else:
            result = "Pontuação baixa em relação à doença."
        return result

    @property
    def score_knowledge_text(self):
        count = self.score_dicotomic
        if count <= 4:
            return "Conhecimento Baixo"
        elif 4 < count <= 8:
            return "Conhecimento Moderado"
        elif 8 < count <= 12:
            return "Conhecimento Alto"
        elif 12 < count <= 16:
            return "Conhecimento Muito Alto"
        else:
            return "Fora do intervalo considerado"

    
    @property
    def score_dicotomic_text(self):
        if self.score_weight > 70:
            result = "Atitude positiva em relação à doença."
        else:
            result = "Pontuação baixa em relação à doença."
        return result

    # def calculate_attitude_score(self, responses):
    #
    #     total_score = 0
    #
    #     # Itera sobre as respostas e soma os valores da escala Likert (1 a 5)
    #     for response in responses:
    #         total_score += response['response_score']
    #
    #     # Avalia a atitude com base no escore
    #     if total_score > 70:
    #         attitude = "Atitude positiva em relação ao diabetes."
    #     else:
    #         attitude = "Atitude negativa em relação ao diabetes."
    #
    #     return total_score, attitude

    class Meta:
        db_table = "answer_sheets"
        verbose_name = "Gabarito"
        verbose_name_plural = "Gabaritos"
        ordering = ["-created_at"]


class Answer(models.Model):
    # user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    answer_sheet = models.ForeignKey(
        AnswerSheet,
        verbose_name="Gabarito",
        related_name="sheet_answers",
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        verbose_name="Questão",
        related_name="question_answers",
        on_delete=models.CASCADE,
    )
    choice = models.ForeignKey(
        Choice,
        verbose_name="Alternativa",
        related_name="choice_answers",
        on_delete=models.CASCADE,
    )
    answered_at = models.DateTimeField("Respondido em", auto_now_add=True)

    created_at = models.DateTimeField("Criado em", editable=False, auto_now_add=True)
    updated_at = models.DateTimeField("Alterado em", editable=False, auto_now=True)

    def __str__(self):
        return f"User: {self.answer_sheet.user.email}, Question: {self.question.text}, Choice: {self.choice.text}"

    class Meta:
        unique_together = ("answer_sheet", "question")
        db_table = "answers"
        verbose_name = "Resposta"
        verbose_name_plural = "Respostas"
        ordering = ["-created_at"]
