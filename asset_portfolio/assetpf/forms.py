from django import forms
from assetpf.models import AddPortfolio,PersonalInfo
from django.db.models import fields

class AddPortfolioForm(forms.ModelForm):
    class Meta:
        model=AddPortfolio
        fields='__all__'
        widgets={
            'date':forms.DateInput(attrs={'class':'form-control'}),
            'objective':forms.TextInput(attrs={'class':'form-control'}),
            'income':forms.NumberInput(attrs={'class':'form-control'}),
            'expense':forms.NumberInput(attrs={'class':'form-control'}),
            
        }

    

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model=PersonalInfo
        fields='__all__' 