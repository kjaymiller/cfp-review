from django import forms
from .models import Review, Proposal


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["score", "feedback"]
        widgets = {
            "feedback": forms.Textarea(attrs={"rows": 4}),
        }


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ["title", "abstract", "private_notes", "tags", "status"]
