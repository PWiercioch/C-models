from django import forms
from .models import Simulation, State, Force, Part, Type
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
    full_name = forms.CharField(label='test', max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'X_XX', 'required pattern': '[A-Za-z]{1}_\d+'}))

    # def __init__(self, *args, **kwargs):
    #     print(f"{kwargs}")
    #     super(PartForm, self).__init__(*args, **kwargs)

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
        attrs={'placeholder': 'C_X_XX', 'required': True, 'required pattern': '[cC]_[A-Za-z]{1}_\d+'}))
    description = forms.CharField(widget=forms.Textarea, required=False)
    post_processing = forms.CharField(max_length=500, required=False)
    balance = forms.FloatField(required=False)
    massflow = forms.FloatField(required=False)


class StateForm(forms.ModelForm):
    state = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(StateForm, self).__init__(*args, **kwargs)
        choices = State.objects.all()
        self.fields['state'].choices = list(zip(iter(choices), iter(choices)))  # Creates list of doubled tuples from list


    class Meta:
        model = State
        fields = ['state']


class SimulationMultiForm(MultiModelForm):

    form_classes = {
        'simulation': SimulationForm,
        'chassis': ChassisMultiForm,
        'df': ForceForm,
        'drag': ForceForm,
        'state': StateForm
    }

    def __init__(self, *args, **kwargs):
        super(SimulationMultiForm, self).__init__(*args, **kwargs)
        for part, initial in kwargs['initial'].items():
            if part == "prefix":
                continue
            self.forms['chassis'].forms[part].fields['full_name'].widget.attrs['value'] = f"{initial['main_v']}_{initial['sub_v']}"

