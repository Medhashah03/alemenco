from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image']


class ImageReq(forms.ModelForm):
    class Meta:
        model= Image
        fields =['title']
