from django import forms
from .models import *
from django.contrib.auth.hashers import make_password
from django.forms import modelformset_factory

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number','password' ,'job_position', 'email', 'age']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'NAME', 'class': 'form-control selecttype'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'PHONE NUMBER', 'class': 'form-control'}),
            'password':forms.TextInput(attrs={'placeholder':'ENTER PASSWORD','class': 'form-control password'}),
            'job_position': forms.TextInput(attrs={'placeholder': 'JOB POSITION', 'class': 'form-control jobposition'}),
            'email': forms.EmailInput(attrs={'placeholder': 'EMAIL ADDRESS', 'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'placeholder': 'AGE', 'class': 'form-control'}),
        }

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.password = make_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            customer.save()
        return customer
    
class Loginform(forms.Form):
    username = forms.CharField(
        label="User Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Name'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your password'
        })
    )

class FinancialStatementForm(forms.ModelForm):
    # Override BooleanFields with Yes/No radio buttons
    def clean_is_saving_enough(self):
        value = self.cleaned_data['is_saving_enough']
        return value == 'True'

    def clean_is_overspending(self):
        value = self.cleaned_data['is_overspending']
        return value == 'True'

    def clean_is_debt_hurting(self):
        value = self.cleaned_data['is_debt_hurting']
        return value == 'True'


    class Meta:
        model = Finacial_statements
        exclude = ['name']
        fields = [
            'name',
            'income',
            'expenses',
            'assets',
            'investment_risk',
            'emergency_savings',
            'is_saving_enough',
            'is_overspending',
            'is_debt_hurting',
        ]
        labels = {
            'income': 'Monthly Income',
            'expenses': 'Monthly Expenses',
            'assets': 'Total Assets',
            'investment_risk': 'Investment Risk Level',
            'emergency_savings': 'Emergency Savings Amount',
        }
        widgets = {
            'income': forms.NumberInput(attrs={'placeholder': 'Monthly Income'}),
            'expenses': forms.NumberInput(attrs={'placeholder': 'Monthly Expenses'}),
            'assets': forms.NumberInput(attrs={'placeholder': 'The Asset Money (in Rs)'}),
            'emergency_savings': forms.NumberInput(attrs={'placeholder': 'Total Money (in Rs)'}),
            'investment_risk': forms.Select(choices=[
                ("low", "Low"),
                ("medium", "Medium"),
                ("high", "High"),
            ]),
        }

LiabilityFormSet = modelformset_factory(Liability, 
    fields=['liability_type','amount'], 
    extra=2
    )
FinancialGoalsFormSet = modelformset_factory(Financial_goals, fields=['goal_type'], extra=2,)