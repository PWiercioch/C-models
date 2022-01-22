from django import forms
from .models import Simulation, Chassis, Force, Part, Type
from betterforms.multiform import MultiModelForm


class ChassisForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = '__all__'

class ForceForm(forms.ModelForm):
    class Meta:
        model = Force
        fields = ['body', 'front_wing', 'rear_wing', 'sidepod', 'diffuser', 'suspension', 'wheel_front', 'wheel_rear']

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = '__all__'

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = '__all__'

class ChassisMultiForm(MultiModelForm):
    form_classes = {
        'body': PartForm,
        'front_wing': PartForm,
        'rear_wing': PartForm,
        'sidepod': PartForm,
        'diffuser': PartForm,
        'suspension': PartForm,
        'wheel_front': PartForm,
        'wheel_rear': PartForm,
    }

class SimulationMultiForm(MultiModelForm):
    form_classes = {
        'chassis': ChassisMultiForm,
        'df': ForceForm,
        'drag': ForceForm,
    }

''''
class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = '__all__'


class SimulationMetaForm(forms.ModelForm):
    class Meta:
        model = SimulationMeta
        fields = ['description']


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
'''
