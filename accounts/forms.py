from django import forms
from accounts.models import CustomUser

class UserSignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['username', 'email']  # Add any additional fields you want for both users and dealers.

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        print(user)
        print(self.cleaned_data["password1"], 'password')
        user.set_password(self.cleaned_data["password1"])
        user.role = 'customer'  # Default role for general users
        if commit:
            user.save()
        return user


class DealerSignupForm(UserSignupForm):
    def save(self, commit=True):
        dealer = super().save(commit=False)
        dealer.role = 'dealer'  # Role set to dealer for this form
        if commit:
            dealer.save()
        return dealer
