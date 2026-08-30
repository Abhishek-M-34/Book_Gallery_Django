from django import forms
from django.contrib.auth.models import User

from .models import Book

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput)
    confirm_password = forms.CharField(widget= forms.PasswordInput)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username','email','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Password do not match.")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

class BookForm(forms.ModelForm):
    price = forms.DecimalField(min_value=0.01, decimal_places=2, max_digits=10)
    class Meta:
        model = Book
        fields = ['title', 'description', 'price']

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 2:
            raise forms.ValidationError("Book title must contain at least 2 characters.")
        return title
    
    def clean_description(self):
        description = self.cleaned_data['description'].strip()
        if len(description) < 10:
            raise forms.ValidationError("Description must contain at least 10 characters.")
        return description

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price