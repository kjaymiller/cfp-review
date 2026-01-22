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
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "tags":  # Checkboxes shouldn't get form-control class
                existing_class = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = f"{existing_class} form-control".strip()
            if field_name == "abstract":
                field.widget.attrs["rows"] = 5
            if field_name == "private_notes":
                field.widget.attrs["rows"] = 3
