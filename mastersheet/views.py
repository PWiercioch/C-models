from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import request

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Simulation

class CustomLoginView(LoginView):
    template_name = 'mastersheet/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('simulations')


class SimulationList(LoginRequiredMixin, ListView):
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
    context_object_name = 'simulation'
    # template_name = 'mastersheet/simulation_detail.html'


class SimulationDelete(LoginRequiredMixin, DeleteView):
    model = Simulation
    context_object_name = 'simulation'

    success_url = reverse_lazy('simulations')


class SimulationUpdate(LoginRequiredMixin, UpdateView):
    model = Simulation
    fields = ['chassis_name', 'description', 'front_wing_name', 'rear_wing_name',
              'sidepod_name', 'diffuser_name', 'undertray_name', 'nose_name', 'front_wing_df','rear_wing_df',
              'sidepod_df', 'diffuser_df', 'undertray_df', 'nose_df', 'front_wing_drag',
              'rear_wing_drag','sidepod_drag', 'diffuser_drag', 'undertray_drag', 'nose_drag']
    success_url = reverse_lazy('simulations')

class SimulationCreate(LoginRequiredMixin, CreateView):

    context_object_name = 'simulation'
    model = Simulation

    fields = ['chassis_name', 'description', 'front_wing_name', 'rear_wing_name',
              'sidepod_name', 'diffuser_name', 'undertray_name', 'nose_name', 'front_wing_df', 'rear_wing_df',
              'sidepod_df', 'diffuser_df', 'undertray_df', 'nose_df', 'front_wing_drag',
              'rear_wing_drag', 'sidepod_drag', 'diffuser_drag', 'undertray_drag', 'nose_drag']
    success_url = reverse_lazy('simulations')

    def form_valid(self, form):
        test = self.request.POST.get('Read')

        form.instance.user = self.request.user
        return super(SimulationCreate, self).form_valid(form)
