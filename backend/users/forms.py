from django import forms
from .models import StudentGroup


class StudentImportForm(forms.Form):
    group = forms.ModelChoiceField(queryset=StudentGroup.objects.all(), label="Select Group", required=True)
    file = forms.FileField(label="Excel File")