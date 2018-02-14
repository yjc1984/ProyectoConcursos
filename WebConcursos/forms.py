from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import models, UsuarioCustom
from WebConcursos import models
from django.contrib.auth import password_validation

class UserRegisterFormCustom(UserCreationForm):
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    #username = forms.EmailField(required=True)
    password1 = forms.CharField(strip=False,widget=forms.PasswordInput,)
    password2 = forms.CharField(strip=False,widget=forms.PasswordInput,)

    class Meta:
        model = UsuarioCustom
        fields = ('username','password1','password2', 'first_name','last_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set the user_id as an attribute of the form
        #self.user_id = user_id

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
        # Validate the password after self.instance is updated with form data
        # by super().
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
