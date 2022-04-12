from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import request
from django.views.generic import edit as edit
from django.db.models import Q
from django.core import serializers
from copy import copy

from django.core import serializers

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Simulation, Chassis, Part, Type, Force

from . import handle_uploaded_file

from .forms import SimulationMultiForm, PartForm

import re

class CustomLoginView(LoginView):
    template_name = 'mastersheet/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('simulations')

class SimulationList(ListView):
    template_name = 'mastersheet/simulation_list.html'
    model = Simulation
    context_object_name = 'simulations'
    chassis_model = Chassis
    chassis_data = serializers.serialize("python", chassis_model.objects.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['simulations'] = context['simulations']  # .filter(user=self.request.user) - to get the user simulations
        # context['simulations'] = context['simulations'].filter(complete=False)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            search_RegEx = re.compile("^(([A-Za-z]*)_)?([A-Za-z])?(_)?(\d+)?$")
            pattern = re.search(search_RegEx, search_input)
            if pattern.group(3):
                context['simulations'] = context['simulations'].filter(main_v=pattern.group(3))

            if pattern.group(5):
                context['simulations'] = context['simulations'].filter(sub_v__startswith=pattern.group(5))

        context['count'] = context['simulations'].count()
        context['search_input'] = search_input

        return context


class SimulationDetail(LoginRequiredMixin, DetailView):
    model = Simulation
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent = Simulation.objects.get(main_v=self.object.main_v, sub_v=self.object.sub_v).parent
        if parent:
            context['parent_slug'] = parent.slug
        return context



class SimulationDelete(LoginRequiredMixin, DeleteView):
    model = Simulation
    context_object_name = 'simulation'

    success_url = reverse_lazy('simulations')


class SimulationUpdate(LoginRequiredMixin, UpdateView):
    model = Simulation
    fields = ['main_v', 'sub_v', 'description', 'post_processing', 'state', 'parent']
    context_object_name = 'simulation'
    template_name = 'mastersheet/simulation_update.html'
    success_url = reverse_lazy('simulations')

    forces = []

    def get_context_data(self, **kwargs):
        context = super(SimulationUpdate, self).get_context_data(**kwargs)
        if self.request.method  == "GET":
            forms = {}
            forces = {}

            forms['body'] = Part.objects.get(id=self.object.chassis.body_id)
            forms['front_wing'] = Part.objects.get(id=self.object.chassis.front_wing_id)
            forms['rear_wing'] = Part.objects.get(id=self.object.chassis.rear_wing_id)
            forms['sidepod'] = Part.objects.get(id=self.object.chassis.sidepod_id)
            forms['diffuser'] = Part.objects.get(id=self.object.chassis.diffuser_id)
            forms['suspension'] = Part.objects.get(id=self.object.chassis.suspension_id)
            forms['wheel_front'] = Part.objects.get(id=self.object.chassis.wheel_front_id)
            forms['wheel_rear'] = Part.objects.get(id=self.object.chassis.wheel_rear_id)

            forces['df'] = Force.objects.get(id=self.object.df_id)
            forces['drag'] = Force.objects.get(id=self.object.drag_id)

            # copy original object
            object = copy(self.object)

            for id, part in forms.items():
                self.object = part
                form = edit.model_forms.modelform_factory(Part, fields=['main_v', 'sub_v'])(**self.get_form_kwargs())
                forms[id] = form

            for id, force in forces.items():
                self.object = force
                form = edit.model_forms.modelform_factory(Force, fields='__all__')(**self.get_form_kwargs())
                forces[id] = form

            # Get the original object back
            self.object = object

            self.args = forms
            self.forces = forces

            context['sub_forms'] = self.args
            context['forces'] = self.forces
        return context

    def form_valid(self, form):
        # TODO handle updating submodel
        return super(SimulationUpdate, self).form_valid(form)


class SimulationCreate(FormView):
    context_object_name = 'simulation'
    form_class = SimulationMultiForm
    template_name = 'mastersheet/simulation_form.html'
    success_url = reverse_lazy('simulations')

    def get_initial(self):
        initial = super(SimulationCreate, self).get_initial()
        if self.kwargs['slug'] == "new":
            return {}
        parent = Simulation.objects.get(slug=self.kwargs['slug'])
        initial['body'] = {"main_v": parent.chassis.body.main_v, 'sub_v': parent.chassis.body.sub_v}
        initial['front_wing'] = {"main_v": parent.chassis.front_wing.main_v, 'sub_v': parent.chassis.front_wing.sub_v}
        initial['rear_wing'] = {"main_v": parent.chassis.rear_wing.main_v, 'sub_v': parent.chassis.rear_wing.sub_v}
        initial['sidepod'] = {"main_v": parent.chassis.sidepod.main_v, 'sub_v': parent.chassis.sidepod.sub_v}
        initial['diffuser'] = {"main_v": parent.chassis.diffuser.main_v, 'sub_v': parent.chassis.diffuser.sub_v}
        initial['suspension'] = {"main_v": parent.chassis.suspension.main_v, 'sub_v': parent.chassis.suspension.sub_v}
        initial['wheel_front'] = {"main_v": parent.chassis.wheel_front.main_v, 'sub_v': parent.chassis.wheel_front.sub_v}
        initial['wheel_rear'] = {"main_v": parent.chassis.wheel_rear.main_v, 'sub_v': parent.chassis.wheel_rear.sub_v}
        return initial


    def form_valid(self, form):
        if self.request.POST.get('Read'):
            general = handle_uploaded_file.main(self.request.FILES["general"])
            df = handle_uploaded_file.main(self.request.FILES["df"])
            drag = handle_uploaded_file.main(self.request.FILES["drag"])

            # TODO - move to handle_upladed_file
            form.forms['df'].instance.body = round(float(df[1]), 2)
            form.forms['df'].instance.diffuser = round(float(df[2]), 2)
            form.forms['df'].instance.front_wing = round(float(df[3]), 2)
            form.forms['df'].instance.rear_wing = round(float(df[4]), 2)
            form.forms['df'].instance.sidepod = round(float(df[5]), 2)
            form.forms['df'].instance.suspension = round(float(df[6]), 2)
            form.forms['df'].instance.wheel_front = round(float(df[7]), 2)
            form.forms['df'].instance.wheel_rear = round(float(df[8]), 2)
            form.forms['df'].instance.total = round(float(df[9]), 2)

            form.forms['drag'].instance.body = round(float(drag[1]),2)
            form.forms['drag'].instance.diffuser = round(float(drag[2]), 2)
            form.forms['drag'].instance.front_wing = round(float(drag[3]), 2)
            form.forms['drag'].instance.rear_wing = round(float(drag[4]), 2)
            form.forms['drag'].instance.sidepod = round(float(drag[5]),2)
            form.forms['drag'].instance.suspension = round(float(drag[6]), 2)
            form.forms['drag'].instance.wheel_front = round(float(drag[7]), 2)
            form.forms['drag'].instance.wheel_rear = round(float(drag[8]), 2)
            form.forms['drag'].instance.total = round(float(drag[9]), 2)

            balance = round(float(general[1]), 2)
            massflow = round(float(general[2]), 2)
        else:
            balance = form.data["simulation-balance"]
            massflow = form.data["simulation-massflow"]


        form.forms['drag'].instance.type = Type.objects.get(type='drag')
        form.forms['df'].instance.type = Type.objects.get(type='df')

        drag_form = form.forms['drag'].save()
        df_form = form.forms['df'].save()

        nameRegEx = re.compile("^(([A-Za-z]*)_)?([A-Za-z])_(\d+)$")

        deleted_forms = {}
        saved_forms = {}
        for part_form in form.forms['chassis'].forms:
            part_version = re.search(nameRegEx, form.data[f"{part_form}__chassis-full_name"])
            try:
                deleted_forms[part_form] = Part.objects.get(type=Type.objects.get(type=part_form),
                                    main_v=part_version.group(3).upper(),
                                    sub_v=part_version.group(4))
            except:
                form.forms['chassis'].forms[part_form].instance.type = Type.objects.get(type=part_form)
                form.forms['chassis'].forms[part_form].instance.main_v = part_version.group(3).upper()
                form.forms['chassis'].forms[part_form].instance.sub_v = part_version.group(4)
                saved_forms[part_form] = form.forms['chassis'].forms[part_form]

        if saved_forms:
            for id, p_form in saved_forms.items():
                saved_forms[id] = p_form.save()

        chassis_form = {}
        chassis_form.update(saved_forms)
        chassis_form.update(deleted_forms)

        sim_version = re.search(nameRegEx, form.data["simulation-full_name"])

        chassis_form = Chassis(body=chassis_form['body'],
                               front_wing=chassis_form['front_wing'],
                               rear_wing=chassis_form['rear_wing'],
                               sidepod=chassis_form['sidepod'],
                               diffuser=chassis_form['diffuser'],
                               suspension=chassis_form['suspension'],
                               wheel_front=chassis_form['wheel_front'],
                               wheel_rear=chassis_form['wheel_rear'])
        chassis_form.save()

        if self.kwargs['slug'] != "new":
            parent = Simulation.objects.get(slug=self.kwargs['slug'])
        else:
            parent = None
        simulation = Simulation(main_v=sim_version.group(3).upper(),
                                sub_v=sim_version.group(4),
                                description=form.data["simulation-description"],
                                post_processing=form.data["simulation-post_processing"],
                                slug=sim_version.group(3).upper() + '-' + str(sim_version.group(4)),
                                df=df_form,
                                drag=drag_form,
                                chassis=chassis_form,
                                balance=balance,
                                massflow=massflow,
                                parent=parent)
        # TODO - handle user
        # TODO - add picture

        simulation.save()
        return super(SimulationCreate, self).form_valid(form)
