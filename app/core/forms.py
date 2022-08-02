from django import forms
from django.contrib.auth.models import User


class loginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput({'placeholder':'Username', 'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput({'placeholder':'Password', 'class':'form-control'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None
            if not user or not user.check_password(password):
                raise forms.ValidationError("Usuario o contraseña incorrecto")
            if not user.is_active:
                raise forms.ValidationError("Usuario no activo")
        return super(loginForm, self).clean(*args, **kwargs)