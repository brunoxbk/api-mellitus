from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

@register_snippet
class Treatment(models.Model):
    nome = models.CharField('nome', max_length=55)

    panels = [
        FieldPanel("nome"),
    ]

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "treatments"
        verbose_name = 'Tratamento'
        verbose_name_plural = 'Tratamentos'


class User(AbstractBaseUser, PermissionsMixin):
    '''
        1 Identificação:
        Data de nascimento;
        Tipo de diabetes (  ) tipo 1  (  ) tipo 2
        Tempo de diagnóstico do diabetes (anos)
        Peso
        Altura
        outras doenças.
        Tipo de tratamento:
        (  ) Medicamentos orais 
        (  ) medicamentos orais+ dieta
        (  ) medicamentos orais + insulina
        (  ) insulina
        (  ) medicamentos orais+insulina+dieta
        Você faz uso de bebida alcoólica (sim/ não); 
        Você fuma (sim/não)

    '''

    DIABETES_CHOICES = [
        ("1", "Tipo 1"),
        ("2", "Tipo 2"),
    ]
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    birth = models.DateField('nascimento', null=True, blank=True)
    diabetes = models.CharField(
        'tipo diabetes', max_length=3, choices=DIABETES_CHOICES, null=True, blank=True)
    diagnostico = models.IntegerField('tempo de diagnostico', null=True, blank=True)

    peso = models.IntegerField('peso', null=True, blank=True)

    bebe = models.BooleanField('bebe', null=True, blank=True)
    fuma = models.BooleanField('fuma', null=True, blank=True)

    doencas = models.TextField('doencas', null=True, blank=True)

    tratamentos = models.ManyToManyField(Treatment)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)