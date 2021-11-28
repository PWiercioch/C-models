from django.urls import path
from .views import SimulationList, CustomLoginView, SimulationDetail, SimulationDelete, SimulationUpdate, SimulationCreate, SimulationCreate_2
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name=('login')),
    path('logout/', LogoutView.as_view(next_page='login'), name=('logout')),
    path('', SimulationList.as_view(), name='simulations'),
    path('simulation/<str:pk>/', SimulationDetail.as_view(), name='simulation'),
    path('simulation-create/', SimulationCreate.as_view(), name='simulation-create'),
    path('simulation-update/<str:pk>/', SimulationUpdate.as_view(), name='simulation-update'),
    path('simulation-delete/<str:pk>/', SimulationDelete.as_view(), name='simulation-delete'),
]