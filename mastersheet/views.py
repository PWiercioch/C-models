from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import request
from django.views.generic import edit as edit

from django.core import serializers

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Simulation, Chassis, Part, Type

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


class SimulationList2(LoginRequiredMixin, ListView):
    model = Simulation
    context_object_name = 'simulations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['simulations'] = context['simulations'] #.filter(user=self.request.user) - to get the user simulations
        # context['simulations'] = context['simulations'].filter(complete=False)
        context['count'] = context['simulations'].count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['simulations'] = context['simulations'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        return context


class SimulationDetail(LoginRequiredMixin, DetailView):
    model = Simulation


class SimulationDelete(LoginRequiredMixin, DeleteView):
    model = Simulation
    context_object_name = 'simulation'

    success_url = reverse_lazy('simulations')


class SimulationUpdate(LoginRequiredMixin, UpdateView):
    model = Simulation
    fields = '__all__'
    context_object_name = 'simulation'
    template_name = 'mastersheet/simulation_update.html'
    success_url = reverse_lazy('simulations')

    def get_context_data(self, **kwargs):
        # TODO get a submodel in the context - render in a template
        body = Part.objects.get(id=self.object.chassis.body_id)
        test = edit.model_forms.modelform_factory(Part, fields=['main_v', 'sub_v'])(**self.get_form_kwargs())
        test.instance = body
        context = super(SimulationUpdate, self).get_context_data(**kwargs)
        context['part_form'] = test
        return context

    def form_valid(self, form):
        # TODO handle updating submodel
        return super(SimulationUpdate, self).form_valid(form)


class SimulationCreate(FormView):
    context_object_name = 'simulation'
    form_class = SimulationMultiForm
    template_name = 'mastersheet/simulation_form.html'
    success_url = reverse_lazy('simulations')

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
                                    main_v=part_version.group(3),
                                    sub_v=part_version.group(4))
            except:
                form.forms['chassis'].forms[part_form].instance.type = Type.objects.get(type=part_form)
                form.forms['chassis'].forms[part_form].instance.main_v = part_version.group(3)
                form.forms['chassis'].forms[part_form].instance.sub_v = part_version.group(4)
                saved_forms[part_form] = form.forms['chassis'].forms[part_form]

        if saved_forms:
            for p_form in saved_forms.values():
                p_form.save()

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
        simulation = Simulation(main_v=sim_version.group(3),
                                sub_v=sim_version.group(4),
                                description=form.data["simulation-description"],
                                post_processing=form.data["post_processing"],
                                slug=sim_version.group(3) + '-' + str(sim_version.group(4)),
                                df=df_form,
                                drag=drag_form,
                                chassis=chassis_form,
                                balance=balance,
                                massflow=massflow)
        # TODO - handle user
        # TODO - handle parent simulation
        # TODO - better handle regexes
        # TODO - add simulation state
        # TODO - add picture

        simulation.save()
        return super(SimulationCreate, self).form_valid(form)
