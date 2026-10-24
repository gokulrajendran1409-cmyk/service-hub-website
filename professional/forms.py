
from django import forms
from professional.models import proreg

class proregform(forms.ModelForm):
    class Meta:
        model = proreg
        fields = [
            "name",
            "phone",
            "email",
            "category",
            "upload_doc",
            "id_proof",
            "password",
            "profile_pic",
            "address",
            "service_charge",
            "description",
            "location",
            "experience",
        ]
        widgets = {
            "password": forms.PasswordInput(),
            "description": forms.Textarea(attrs={"rows": 3}),
            "address": forms.Textarea(attrs={"rows": 2}),
        }

