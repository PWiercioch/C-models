from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import request

from django.core import serializers

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Simulation, Chassis, Part, Type

from . import handle_uploaded_file

from .forms import SimulationMultiForm

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
    chassis_model = Chassis
    chassis_data = serializers.serialize("python", chassis_model.objects.all())

    # TODO - handle search


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
    success_url = reverse_lazy('simulations')


class SimulationCreate(FormView):
    context_object_name = 'simulation'
    # TODO - will forms be necessary or should I just do it with models directly
    form_class = SimulationMultiForm
    template_name = 'mastersheet/simulation_form.html'
    success_url = reverse_lazy('simulations')

    def form_valid(self, form):
        if self.request.POST.get('Read'):
            general = handle_uploaded_file.main(self.request.FILES["general"])[0].split(';')
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
            balance = None  # TODO - add to form
            massflow = None

        form.forms['drag'].instance.type = Type.objects.get(type='drag')
        form.forms['df'].instance.type = Type.objects.get(type='df')

        drag_form = form.forms['drag'].save()
        df_form = form.forms['df'].save()

        deleted_forms = {}
        saved_forms = {}
        for part_form in form.forms['chassis'].forms:
            # TODO - make it a global regex, handle prefix
            main_v = re.search('^[A-Za-z]', form.data[f"{part_form}__chassis-full_name"])
            sub_v = re.search('\d+$', form.data[f"{part_form}__chassis-full_name"])
            try:
                deleted_forms[part_form] = Part.objects.get(type=Type.objects.get(type=part_form),
                                    main_v=main_v.group(),
                                    sub_v=sub_v.group())
            except:
                form.forms['chassis'].forms[part_form].instance.type = Type.objects.get(type=part_form)
                form.forms['chassis'].forms[part_form].instance.main_v = main_v.group()
                form.forms['chassis'].forms[part_form].instance.sub_v = sub_v.group()
                saved_forms[part_form] = form.forms['chassis'].forms[part_form]

        saved_forms = form.forms['chassis'].save()

        chassis_form = {}
        chassis_form.update(saved_forms)
        chassis_form.update(deleted_forms)

        # TODO - add simulation name in form
        main_v = re.search('\D+', self.request.POST['sim_name'])
        sub_v = re.search('\d+', self.request.POST['sim_name'])

        chassis_form = Chassis(body=chassis_form['body'],
                               front_wing=chassis_form['front_wing'],
                               rear_wing=chassis_form['rear_wing'],
                               sidepod=chassis_form['sidepod'],
                               diffuser=chassis_form['diffuser'],
                               suspension=chassis_form['suspension'],
                               wheel_front=chassis_form['wheel_front'],
                               wheel_rear=chassis_form['wheel_rear'])
        chassis_form.save()
        simulation = Simulation(main_v=main_v.group().strip('_'),
                                sub_v=sub_v.group(),
                                description=self.request.POST['Description'],
                                slug=main_v.group().strip('_') + '-' + str(sub_v.group()),
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

        simulation.save()  # TODO - why it overwrites model with the same main_v but doesnt work for model forms
        return super(SimulationCreate, self).form_valid(form)
