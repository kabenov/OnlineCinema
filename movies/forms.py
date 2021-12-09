from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserCreationForm, self).__init__(*args, **kwargs)

        username_widget = forms.TextInput(attrs={'placeholder': 'Username'})
        username_field = forms.CharField(label="Username", widget=username_widget)
        self.fields["username"] = username_field

        login_widget = forms.EmailInput(attrs={'placeholder': 'Email'})
        login_field = forms.EmailField(label="Email", widget=login_widget)
        self.fields["email"] = login_field

        pass1_widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        pass1_field = forms.CharField(label="Password", widget=pass1_widget)
        self.fields["password1"] = pass1_field

        pass2_widget = forms.PasswordInput(attrs={'placeholder': 'Re-Password'})
        pass2_field = forms.CharField(label="Re-Password", widget=pass2_widget)
        self.fields["password2"] = pass2_field

