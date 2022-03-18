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
        fields = '__all__'

# TODO - will clean works also with normal Form??
class PartForm(forms.ModelForm):
    # TODO - add custom error messages
    full_name = forms.CharField(label='test', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'test', 'required pattern': '[A-Za-z]{1}_\d+'}))

    # def clean(self):  # allows to validate at the deeper level - check if already exists in db
    #     return self.cleaned_data
    #     # raise forms.ValidationError({"full_name": "error"})
    #     cleaned_data = super(PartForm, self).clean()
    #     # main_v = self.cleaned_data.get('main_v')
    #     # try:
    #     #     # match = Part.objects.get(main_v=main_v)
    #     #     raise forms.ValidationError({"main_v": "error"})
    #     # except Part.DoesNotExist:
    #     #     return main_v

    class Meta:
        model = Part
        fields = ['full_name']
    #
    #     error_messages = {  # TODO - this should work
    #         'full_name': {
    #             'required': ("This writer's name is too long."),
    #         },
    #     }

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

class SimulationForm(forms.Form):
    full_name = forms.CharField(label='test', max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'test', 'required pattern': '[A-Za-z]{1}_\d+'}))
    description = forms.CharField(widget=forms.Textarea, required=False)
    balance = forms.FloatField(required=False)
    massflow = forms.FloatField(required=False)

    class Meta:
        error_messages = {  # TODO - this should work
            'full_name': {
                'required': ("This writer's name is too long."),
            },
        }

class SimulationMultiForm(MultiModelForm):

    form_classes = {
        'simulation': SimulationForm,
        'chassis': ChassisMultiForm,
        'df': ForceForm,
        'drag': ForceForm,
    }
