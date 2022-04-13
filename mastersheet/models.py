from django.db import models
import re
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User


# Create your models here.
class Type(models.Model):
    type = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=20)

    def __str__(self):
        return self.abbreviation

class State(models.Model):
    state = models.CharField(max_length=40)

    def __str__(self):
        return self.state


class Part(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True)

    main_v = models.CharField(max_length=5)
    sub_v = models.IntegerField()

    def __str__(self):
        return str(self.type) + "_" + self.main_v + '_' + str(self.sub_v)

    class Meta:
        ordering = ['main_v', 'sub_v']
        unique_together = ('type', 'main_v', 'sub_v')


class Force(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True, null=True)
    body = models.FloatField(blank=True, null=True)
    diffuser = models.FloatField(blank=True, null=True)
    front_wing = models.FloatField(blank=True, null=True)
    rear_wing = models.FloatField(blank=True, null=True)
    sidepod = models.FloatField(blank=True, null=True)
    suspension = models.FloatField(blank=True, null=True)
    wheel_front = models.FloatField(blank=True, null=True)
    wheel_rear = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.type) + str(self.id)


class Chassis(models.Model):
    body = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True, related_name='b')
    front_wing = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True, related_name='fw')
    rear_wing = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True, related_name='rw')
    sidepod = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True, related_name='s')
    diffuser = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True, related_name='d')
    suspension = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True, related_name='su')
    wheel_front = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True, related_name='wf')
    wheel_rear = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, null=True, related_name='wr')


class Simulation(models.Model):
    main_v = models.CharField(max_length=10)
    sub_v = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    post_processing = models.CharField(max_length=500, null=True, blank=True)
    report = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField(primary_key=True)

    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)
    df = models.ForeignKey(Force, on_delete=models.SET_NULL, blank=True, null=True, related_name='df')
    drag = models.ForeignKey(Force, on_delete=models.SET_NULL, blank=True, null=True, related_name='drag')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    chassis = models.ForeignKey(Chassis, on_delete=models.SET_NULL, null=True, blank=True)
    balance = models.FloatField(blank=True, null=True)
    massflow = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.main_v + '_' + str(self.sub_v)


    class Meta:
        db_table = 'Simulation'
        unique_together = ('main_v', 'sub_v')
        ordering = ['main_v', 'sub_v']

        managed = True
        # This requires manual creation(and updates probably) of the table
        '''
        sqlite3  db.sqlite3
        
        CREATE TABLE Simulation (
        main_v, 
        sub_v,
        description, 
        slug,
        df_id,
        drag_id,
        parent_id,
        chassis_id, 
        balance,
        massflow,
        PRIMARY KEY (main_v, sub_v),
        FOREIGN KEY (df_id) REFERENCES mastersheet_force(id),
        FOREIGN KEY (drag_id) REFERENCES mastersheet_force(id),
        FOREIGN KEY (main_v, sub_v) REFERENCES Simulation(main_v, sub_v),
        FOREIGN KEY (chassis_id) REFERENCES mastersheet_chassis(id)
        );
        '''
