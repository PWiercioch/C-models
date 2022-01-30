from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import request

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Simulation, Chassis

from . import handle_uploaded_file

from .forms import SimulationMultiForm

import re

class CustomLoginView(LoginView):
    template_name = 'mastersheet/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return 0 #reverse_lazy('simulations')

class SimulationList(ListView):
    template_name = 'mastersheet/simulation_list.html'
    model = Simulation


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
    # context_object_name = 'simulation'
    # template_name = 'mastersheet/simulation_detail.html'


class SimulationDelete(LoginRequiredMixin, DeleteView):
    model = Simulation
    context_object_name = 'simulation'

    success_url = reverse_lazy('simulations')


class SimulationUpdate(LoginRequiredMixin, UpdateView):
    model = Simulation
    fields = '__all__'
    success_url = reverse_lazy('simulations')
    '''
    fields = ['chassis_name', 'description', 'front_wing_name', 'rear_wing_name',
              'sidepod_name', 'diffuser_name', 'undertray_name', 'nose_name', 'front_wing_df','rear_wing_df',
              'sidepod_df', 'diffuser_df', 'undertray_df', 'nose_df', 'front_wing_drag',
              'rear_wing_drag','sidepod_drag', 'diffuser_drag', 'undertray_drag', 'nose_drag']
              '''

class SimulationCreate(FormView):
    context_object_name = 'simulation'
    form_class = SimulationMultiForm
    template_name = 'mastersheet/simulation_form.html'
    success_url = reverse_lazy('simulations')

    def form_valid(self, form):
        if self.request.POST.get('Read'):
            general = handle_uploaded_file.main(self.request.FILES["general"])[0].split(';')
            df = handle_uploaded_file.main(self.request.FILES["df"])
            drag = handle_uploaded_file.main(self.request.FILES["drag"])

            # TODO - check this three or four times!!!!!

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

        main_v = re.search('\D+', self.request.POST['sim_name'])
        sub_v = re.search('\d+', self.request.POST['sim_name'])
        sub_form = form.save()
        chassis_form = Chassis(body=sub_form['chassis']['body'],
                               front_wing=sub_form['chassis']['front_wing'],
                               rear_wing=sub_form['chassis']['rear_wing'],
                               sidepod=sub_form['chassis']['sidepod'],
                               diffuser=sub_form['chassis']['diffuser'],
                               suspension=sub_form['chassis']['suspension'],
                               wheel_front=sub_form['chassis']['wheel_front'],
                               wheel_rear=sub_form['chassis']['wheel_rear'])
        chassis_form.save()
        simulation = Simulation(main_v=main_v.group().strip('_'),
                                sub_v=sub_v.group(),
                                description=self.request.POST['Description'],
                                slug=main_v.group().strip('_') + '-' + str(sub_v.group()),
                                df=sub_form['df'],
                                drag=sub_form['drag'],
                                chassis=chassis_form,
                                balance=round(float(general[1]), 2),
                                massflow=round(float(general[2]), 2))
        # TODO - handle user
        # TODO - handle parent simulation

        simulation.save()
        return super(SimulationCreate, self).form_valid(form)
