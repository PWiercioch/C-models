from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class SimulationMeta(models.Model):
    description = models.TextField(null=True, blank=True)
    # complete = models.BooleanField(default=False) # might be used in te future to prompt user to finish simulation
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)


class FrontWing(models.Model):
    name = models.CharField(max_length=10)
    df = models.FloatField(blank=True)
    drag = models.FloatField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class RearWing(models.Model):
    name = models.CharField(max_length=10)
    df = models.FloatField(blank=True)
    drag = models.FloatField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Sidepod(models.Model):
    name = models.CharField(max_length=10)
    df = models.FloatField(blank=True)
    drag = models.FloatField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Diffuser(models.Model):
    name = models.CharField(max_length=10)
    df = models.FloatField(blank=True)
    drag = models.FloatField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Suspension(models.Model):
    name = models.CharField(max_length=10)
    df = models.FloatField(blank=True)
    drag = models.FloatField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Undertray(models.Model):
    name = models.CharField(max_length=10)
    df = models.FloatField(blank=True)
    drag = models.FloatField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Nose(models.Model):
    name = models.CharField(max_length=10)
    df = models.FloatField(blank=True)
    drag = models.FloatField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class WheelFront(models.Model):
    name = models.CharField(max_length=10)
    df = models.FloatField(blank=True)
    drag = models.FloatField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class WheelRear(models.Model):
    name = models.CharField(max_length=10)
    df = models.FloatField(blank=True)
    drag = models.FloatField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Simulation(models.Model):
    name = models.CharField(primary_key=True, max_length=10)

    front_wing = models.OneToOneField(FrontWing, on_delete=models.CASCADE, blank=True)
    rear_wing = models.OneToOneField(RearWing, on_delete=models.CASCADE, blank=True)
    sidepod = models.OneToOneField(Sidepod, on_delete=models.CASCADE, blank=True)
    diffuser = models.OneToOneField(Diffuser, on_delete=models.CASCADE, blank=True)
    undertray = models.OneToOneField(Undertray, on_delete=models.CASCADE, blank=True)
    nose = models.OneToOneField(Nose, on_delete=models.CASCADE, blank=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

