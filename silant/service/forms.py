from django import forms
from .models import *

class BaseForm(forms.ModelForm):
    class Meta:
        abstract = True
        model = None
        fields = '__all__'

class MaintenanceForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Maintenance
        widgets = {
            'type': forms.RadioSelect()
        }

class ComplaintForm(BaseForm):
    class Meta(BaseForm.Meta):
        model = Complaint

