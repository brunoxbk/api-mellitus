# myapp/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm

class CustomUserEditForm(UserEditForm):
    # status = forms.ModelChoiceField(queryset=MembershipStatus.objects, required=True, label=_("Status"))

    # Use ModelForm's automatic form fields generation for the model's `country` field,
    # but use an explicit custom form field for `status`.
    class Meta(UserEditForm.Meta):
        fields = UserEditForm.Meta.fields | {
            "bebe", "fuma", "diagnostico", "diabetes",
            "peso", "doencas", "tratamentos"
        }


class CustomUserCreationForm(UserCreationForm):
    # status = forms.ModelChoiceField(queryset=MembershipStatus.objects, required=True, label=_("Status"))

    # Use ModelForm's automatic form fields generation for the model's `country` field,
    # but use an explicit custom form field for `status`.
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields | {
            "bebe", "fuma", "diagnostico", "diabetes",
            "peso", "doencas", "tratamentos"
        }