from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, required=True, label="Full name",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'border-radius:10px;'}))

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get('full_name')
        # Розбиваємо повне ім'я на first_name і last_name (простіше - перше слово у first_name, решта у last_name)
        names = full_name.strip().split(' ', 1)
        user.first_name = names[0]
        if len(names) > 1:
            user.last_name = names[1]
        else:
            user.last_name = ''
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['style'] = 'border-radius: 10px; color: #444'

class UpdateFullNameForm(forms.Form):
    full_name = forms.CharField(max_length=150, required=True, label="Full name",
                                widget=forms.TextInput(attrs={'class': 'form-control'}))