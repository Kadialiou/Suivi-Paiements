from django import forms
from .models import ClientPaiement
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ClientPaiementForm(forms.ModelForm):
    class Meta:
        model = ClientPaiement
        fields = ['nom', 'prenom', 'montant_demande', 'montant_verse']

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requis.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(InscriptionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


