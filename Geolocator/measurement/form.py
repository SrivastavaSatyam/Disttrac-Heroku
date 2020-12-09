from django import forms
from measurement.models import Mes



class MeasurementModelForm(forms.ModelForm):
    class Meta:
        model=Mes
        fields =('Location','Destination',)
        




