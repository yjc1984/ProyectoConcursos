from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import models, UsuarioCustom
from WebConcursos import models
from django.contrib.auth import password_validation, authenticate
from django.utils.text import capfirst
import unicodedata


# UserRegisterFormCustom funciona le registro pero no la autenticacion
class UserRegisterFormCustom(UserCreationForm):
    class Meta:
        model = UsuarioCustom
        fields = ('first_name','last_name','username','password1','password2','Rol','Empresa',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


## UserCreationCustom funciona con nombres y apellidos pero sin empresa ni rol
class UserCreationCustom(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','password1','password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class FormCrearConcurso(forms.ModelForm):
	class Meta:
		model = models.Concurso
		fields = ['nombre','fecha_inicio','fecha_fin','valor_pagar', 'texto_voz','recomendaciones',]
		widgets = {
		'fecha_fin' : forms.DateTimeInput(attrs={'placeholder': '2006-10-25' , 'id': 'fecha_fin' , 'onchange': 'return validacion(this.value)' }),
		'fecha_inicio' : forms.DateTimeInput(attrs={'placeholder': '2006-10-25' , 'id': 'fecha_inicio' , 'onchange': 'return validacion(this.value)' }),
		'texto_voz' :  forms.Textarea(attrs={'rows':10, 'cols':50}),
		'recomendaciones' :  forms.Textarea(attrs={'rows':10, 'cols':50}),
		}

class FormEditarConcurso(forms.ModelForm):
	class Meta:
		model = models.Concurso
		fields = ['nombre','fecha_inicio','fecha_fin','valor_pagar', 'texto_voz','recomendaciones',]
		widgets = {
		'fecha_fin' : forms.DateTimeInput(attrs={'placeholder': '2006-10-25' , 'id': 'fecha_fin' , 'onchange': 'return validacion(this.value)' }),
		'fecha_inicio' : forms.DateTimeInput(attrs={'placeholder': '2006-10-25' , 'id': 'fecha_inicio' , 'onchange': 'return validacion(this.value)' }),
		'texto_voz' :  forms.Textarea(attrs={'rows':10, 'cols':50}),
		'recomendaciones' :  forms.Textarea(attrs={'rows':10, 'cols':50}),
		}