from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import WasteEntry

class RegistrationForm(UserCreationForm):

    flat_number = forms.CharField(
        max_length=20,
        help_text="Enter your flat number (e.g., A-101, B-205)"
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'flat_number']

    def clean_flat_number(self):
        flat_number = self.cleaned_data.get('flat_number')
        from .models import Household
        if Household.objects.filter(flat_number=flat_number).exists():
            raise forms.ValidationError("This flat number is already registered.")
        return flat_number

class WasteEntryForm(forms.ModelForm):

    class Meta:
        model = WasteEntry
        fields = ['waste_type', 'notes']
        widgets = {
            'waste_type': forms.RadioSelect(),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional notes...'}),
        }
