from django import forms
from .models import Employee, Visitor, Visite, Courrier
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class EmployeeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    role = forms.CharField(required=False)
    class Meta:
        model = Employee
        fields = ['email', 'name', 'contact', 'password', 'role']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

 
    def save(self, commit=True):
        employee = super(EmployeeForm, self).save(commit=False)
        employee.set_password(self.cleaned_data['password'])
        if commit:
            employee.save()
        return employee

    def update(self, old_pass, commit=True):
        employee = super(EmployeeForm, self).save(commit=False)

        if self.cleaned_data.get("email"):
            employee.email = self.cleaned_data["email"]
        if self.cleaned_data.get("contact"):
            employee.contact = self.cleaned_data["contact"]
        if self.cleaned_data.get("name"):
            employee.name = self.cleaned_data["name"]
        if self.cleaned_data.get("role"):
            employee.role = self.cleaned_data["role"]
        
        employee.password = old_pass
#
        if commit:
            employee.save()
        return employee

class EmployeeAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['name', 'contact', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VisiteForm(forms.ModelForm):
    class Meta:
        model = Visite
        fields = ['visiteur', 'employee', 'objet', 'date_debut', 'date_fin']
        widgets = {
            'visiteur': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'objet': forms.TextInput(attrs={'class': 'form-control'}),
            'date_debut': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'date_fin': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(VisiteForm, self).__init__(*args, **kwargs)
        self.fields['date_fin'].required = False

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get("date_debut")
        date_fin = cleaned_data.get("date_fin")

        if date_fin and date_debut and date_fin < date_debut:
            raise ValidationError(_('La date de fin doit être après la date de début.'))

        return cleaned_data

class CourrierForm(forms.ModelForm):
    class Meta:
        model = Courrier
        fields = ('expediteur', 'destinataire', 'type_courrier', 'date_reception', 'reference_courrier')
        widgets = {
            'expediteur': forms.TextInput(attrs={'class': 'form-control'}),
            'destinataire': forms.TextInput(attrs={'class': 'form-control'}),
            'type_courrier': forms.TextInput(attrs={'class': 'form-control'}),
            'date_reception': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reference_courrier': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CourrierReceptionForm(forms.ModelForm):
    class Meta:
        model = Courrier
        fields = ['est_recu']
