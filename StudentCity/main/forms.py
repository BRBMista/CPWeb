from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Student


class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('slug', 'owner')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'visa_ending': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.replace('-', '').isalpha():
            raise forms.ValidationError('Недопустимые символы в имени')
        return first_name

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('nation') and not cleaned_data.get('visa_num'):
            self.add_error('visa_num', 'Для иностранного студента укажите номер визы')
        return cleaned_data


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {'email': 'Email'}


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
