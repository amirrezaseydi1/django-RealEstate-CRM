from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget
from ckeditor.widgets import CKEditorWidget

# class Customerform(forms.ModelForm):
#     class Meta:
#         model =Costomer
#         fields = [
#             'name',
#             'phone',
#             'description',
#         ]
#         widgets ={
#             'name': forms.TextInput(attrs={'placeholser':'نام مشتری'})
#         }


# class CustomerRequestForm(forms.ModelForm):
#
#     class Meta:
#         model =CuostomerRequest
#         # fields = ['']
class FollowUpForm(forms.ModelForm):
    note = forms.CharField(
        widget=CKEditorWidget(config_name='default'),
        label="یادداشت پیگیری"
    )

    class Meta:
        model = RequestFollowUp
        fields = ['note']
