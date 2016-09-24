from django import forms
from . import models

class VirtualFixForm(forms.ModelForm):
    class Meta:
        model = models.VirtualFix
        fields = ['title','patch']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'patch': forms.Textarea(attrs={'data-code-input': {}}),
        }