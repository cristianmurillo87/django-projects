from django import forms
from django.core.exceptions import ValidationError

from .models import Note


class NotesForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = (
            "title",
            "text",
        )
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control my-5"}),
            "text": forms.Textarea(attrs={"class": "form-control my-5"}),
        }
        labels = {"text": "Write your thoughts here"}

    def clean_title(self):
        title = self.cleaned_data["title"]
        if "Django" not in title:
            raise ValidationError("Only notes about Django are accepted!")
        return title
