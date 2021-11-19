from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Simulation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    chassis_name = models.CharField(primary_key=True, max_length=10)
    description = models.TextField(null=True, blank=True)
    # complete = models.BooleanField(default=False) # might be used in te future to prompt user to finish simulation
    created = models.DateTimeField(auto_now_add=True)

    front_wing_name = models.CharField(max_length=10)
    rear_wing_name = models.CharField(max_length=10)
    sidepod_name = models.CharField(max_length=10)
    diffuser_name = models.CharField(max_length=10)
    undertray_name = models.CharField(max_length=10)
    nose_name = models.CharField(max_length=10)

    front_wing_df = models.FloatField(blank=True)
    rear_wing_df = models.FloatField(blank=True)
    sidepod_df = models.FloatField(blank=True)
    diffuser_df = models.FloatField(blank=True)
    undertray_df = models.FloatField(blank=True)
    nose_df = models.FloatField(blank=True)

    front_wing_drag = models.FloatField(blank=True)
    rear_wing_drag = models.FloatField(blank=True)
    sidepod_drag = models.FloatField(blank=True)
    diffuser_drag = models.FloatField(blank=True)
    undertray_drag = models.FloatField(blank=True)
    nose_drag = models.FloatField(blank=True)

    def __str__(self):
        return self.chassis_name

    class Meta:
        ordering = ['chassis_name']


from django.db import models

# Create your models here.
