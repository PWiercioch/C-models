from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.http import request

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Simulation

from . import handle_uploaded_file
from . import forms

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

    # success_url = reverse_lazy('simulations')


class SimulationUpdate(LoginRequiredMixin, UpdateView):
    model = Simulation
    fields = '__all__'
    '''
    fields = ['chassis_name', 'description', 'front_wing_name', 'rear_wing_name',
              'sidepod_name', 'diffuser_name', 'undertray_name', 'nose_name', 'front_wing_df','rear_wing_df',
              'sidepod_df', 'diffuser_df', 'undertray_df', 'nose_df', 'front_wing_drag',
              'rear_wing_drag','sidepod_drag', 'diffuser_drag', 'undertray_drag', 'nose_drag']
              '''
    # success_url = reverse_lazy('simulations')


class SimulationCreate(FormView):
    context_object_name = 'simulation'
    '''
    form_class = forms.SimulationMultiForm

    success_url = reverse_lazy('simulations')

    template_name = 'mastersheet/simulation_form.html'

    def form_valid(self, form):
        if self.request.POST.get('Read'):
            df = handle_uploaded_file.main(self.request.FILES["df"])
            drag = handle_uploaded_file.main(self.request.FILES["drag"])

            # TODO - check this three or four times!!!!!

            form.forms['front_wing'].instance.df = round(float(df[3]),
                                       2)  # TODO move to handleuploaded file, add dictionary keys to overwrite form in a loop
            form.forms['rear_wing'].instance.df = round(float(df[4]), 2)
            form.forms['sidepod'].instance.df = round(float(df[5]), 2)
            form.forms['diffuser'].instance.df = round(float(df[2]), 2)
            form.forms['undertray'].instance.df = round(float(df[1]), 2)  # TODO - modify model - there is no undertray in simulation data
            form.forms['nose'].instance.df = round(float(df[6]), 2)  # TODO there is no nose
            form.forms['wheel_front'].instance.df = round(float(df[7]), 2)
            form.forms['wheel_rear'].instance.df = round(float(df[8]), 2)
            form.forms['suspension'].instance.df = round(float(df[8]), 2)

            form.forms['front_wing'].instance.drag = round(float(drag[3]),2)
            form.forms['rear_wing'].instance.drag = round(float(drag[4]), 2)
            form.forms['sidepod'].instance.drag = round(float(drag[5]), 2)
            form.forms['diffuser'].instance.drag = round(float(drag[2]), 2)
            form.forms['undertray'].instance.drag = round(float(drag[1]),2)
            form.forms['nose'].instance.drag = round(float(drag[6]), 2)
            form.forms['wheel_front'].instance.drag = round(float(drag[7]), 2)
            form.forms['wheel_rear'].instance.drag = round(float(drag[8]), 2)
            form.forms['suspension'].instance.drag = round(float(drag[8]), 2)

            # form.instance = post

        pkeys = form.save()
        simulation = Simulation(self.request.POST['simulation_name'],
                                front_wing=pkeys['front_wing'],
                                rear_wing=pkeys['rear_wing'],
                                sidepod=pkeys['sidepod'],
                                diffuser=pkeys['diffuser'],
                                undertray=pkeys['undertray'],
                                nose=pkeys['nose'],
                                suspension=pkeys['suspension'],
                                simulation_meta=pkeys['simulation_meta'])

        # TODO - handle user
        # form.instance.user = self.request.user

        simulation.save()
        return super(SimulationCreate, self).form_valid(form)
        '''


class SimulationCreate_2(LoginRequiredMixin, CreateView):

    context_object_name = 'simulation'
    model = Simulation

    fields = ['name', 'front_wing']

    '''
        fields = ['chassis_name', 'description', 'front_wing_name', 'rear_wing_name',
                  'sidepod_name', 'diffuser_name', 'undertray_name', 'nose_name', 'front_wing_df', 'rear_wing_df',
                  'sidepod_df', 'diffuser_df', 'undertray_df', 'nose_df', 'front_wing_drag',
                  'rear_wing_drag', 'sidepod_drag', 'diffuser_drag', 'undertray_drag', 'nose_drag']
        '''
    # success_url = reverse_lazy('simulations')



    def get_context_data(self, **kwargs):
        context = super(SimulationCreate, self).get_context_data(**kwargs)
        context["Visible2"] = False
        return context

    def form_valid(self, form):
        '''
        if self.request.POST.get('Read'):
            df = handle_uploaded_file.main(self.request.FILES["df"])
            drag = handle_uploaded_file.main(self.request.FILES["drag"])
            post = form.instance

            post.front_wing_df = round(float(df[3]),2)  # TODO move to handleuploaded file, add dictionary keys to overwrite form in a loop
            post.rear_wing_df = round(float(df[4]),2)
            post.sidepod_df = round(float(df[5]),2)
            post.diffuser_df = round(float(df[2]),2)
            post.undertray_df = round(float(df[1]),2)  # TODO - modify model - there is no undertray in simulation data
            post.nose_df = round(float(df[6]),2)

            post.front_wing_drag = round(float(drag[3]),2)
            post.rear_wing_drag = round(float(drag[4]),2)
            post.sidepod_drag = round(float(drag[5]),2)
            post.diffuser_drag = round(float(drag[2]),2)
            post.undertray_drag = round(float(drag[1]),2)
            post.nose_drag = round(float(drag[6]),2)

            form.instance = post
        '''

        form.instance.user = self.request.user
        return super(SimulationCreate, self).form_valid(form)
