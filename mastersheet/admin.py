from django.contrib import admin
from .models import Simulation, SimulationMeta, FrontWing, RearWing, Diffuser, Sidepod, Suspension, Nose, WheelRear, WheelFront

admin.site.register(Simulation)
admin.site.register(SimulationMeta)
admin.site.register(FrontWing)
admin.site.register(RearWing)
admin.site.register(Diffuser)
admin.site.register(Sidepod)
admin.site.register(Suspension)
admin.site.register(Nose)
admin.site.register(WheelRear)
admin.site.register(WheelFront)
