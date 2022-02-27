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
    def clean(self):  # allows to validate at the deeper level - check if already exists in db
        # raise forms.ValidationError({"main_v": "error"})
        pass
        cleaned_data = super(PartForm, self).clean()
        # main_v = self.cleaned_data.get('main_v')
        # try:
        #     # match = Part.objects.get(main_v=main_v)
        #     raise forms.ValidationError({"main_v": "error"})
        # except Part.DoesNotExist:
        #     return main_v

    class Meta:
        model = Part
        fields = ['main_v', 'sub_v']

        widgets = {
            'main_v': forms.TextInput(
                attrs={
                    'placeholder': 'dupa',
                    'oninvalid': "this.setCustomValidity('Cos nie pyklo kurwa')",  # sets custom error message
                    'oninput': "this.setCustomValidity('')",  # hides error message on input
                    'minlength': '2'  # allows to add aditional validators
                },
            ),
        }

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
