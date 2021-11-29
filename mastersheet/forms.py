from django import forms
from .models import Simulation, FrontWing, SimulationMeta, RearWing, Diffuser, Sidepod, Suspension, Undertray, Nose, WheelRear, WheelFront
from betterforms.multiform import MultiModelForm


class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = '__all__'


class SimulationMetaForm(forms.ModelForm):
    class Meta:
        model = SimulationMeta
        fields = '__all__'


class FrontWingForm(forms.ModelForm):
    class Meta:
        model = FrontWing
        fields = '__all__'


class RearWingForm(forms.ModelForm):
    class Meta:
        model = RearWing
        fields = '__all__'


class SidepodForm(forms.ModelForm):
    class Meta:
        model = Sidepod
        fields = '__all__'


class DiffuserForm(forms.ModelForm):
    class Meta:
        model = Diffuser
        fields = '__all__'


class SuspensionForm(forms.ModelForm):
    class Meta:
        model = Suspension
        fields = '__all__'


class UndertrayForm(forms.ModelForm):
    class Meta:
        model = Undertray
        fields = '__all__'


class NoseForm(forms.ModelForm):
    class Meta:
        model = Nose
        fields = '__all__'


class WheelFrontForm(forms.ModelForm):
    class Meta:
        model = WheelFront
        fields = '__all__'


class WheelRearForm(forms.ModelForm):
    class Meta:
        model = WheelRear
        fields = '__all__'


class SimulationMultiForm(MultiModelForm):
    form_classes = {
        'simulation': SimulationForm,
        'front_wing': FrontWingForm,
        'rear_wing': RearWingForm,
        'sidepod': SidepodForm,
        'suspension': SuspensionForm,
        'nose': NoseForm,
        'diffuser': DiffuserForm,
        'wheel_front': WheelFrontForm,
        'wheel_rear': WheelRearForm,
        'undertray': UndertrayForm,
        'simulation_meta': SimulationMetaForm
    }