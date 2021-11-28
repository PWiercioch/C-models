from django import forms
from .models import Simulation, FrontWing
from betterforms.multiform import MultiModelForm


class SimulationForm(forms.ModelForm):

    class Meta:
        model = Simulation
        fields = '__all__'

class FrontWingForm(forms.ModelForm):

    class Meta:
        model = FrontWing
        fields = '__all__'


class SimulationMultiForm(MultiModelForm):
    form_classes = {
        'simulation': SimulationForm,
        'front_wing': FrontWingForm,
    }