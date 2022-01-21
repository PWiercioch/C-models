from django.db import models
from django.contrib.auth.models import User


# Create your models here.
'''
class SimulationMeta(models.Model):
    description = models.TextField(null=True, blank=True)
    # complete = models.BooleanField(default=False) # might be used in te future to prompt user to finish simulation
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)


class FrontWing(models.Model):
    id = models.AutoField(primary_key=True)
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

    simulation_meta = models.ForeignKey(SimulationMeta, on_delete=models.CASCADE, blank=True)
    front_wing = models.ForeignKey(FrontWing, on_delete=models.CASCADE, blank=True)
    rear_wing = models.ForeignKey(RearWing, on_delete=models.CASCADE, blank=True)
    sidepod = models.ForeignKey(Sidepod, on_delete=models.CASCADE, blank=True)
    diffuser = models.ForeignKey(Diffuser, on_delete=models.CASCADE, blank=True)
    undertray = models.ForeignKey(Undertray, on_delete=models.CASCADE, blank=True)
    nose = models.ForeignKey(Nose, on_delete=models.CASCADE, blank=True)
    suspension = models.ForeignKey(Suspension, on_delete=models.CASCADE, blank=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

'''
class Type(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type


class Part(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True)

    main_v = models.CharField(max_length=5)
    sub_v = models.IntegerField()

    class Meta:
        ordering = ['main_v', 'sub_v']


class Force(models.Model):
    body = models.FloatField(blank=True)
    diffuser = models.FloatField(blank=True)
    front_wing = models.FloatField(blank=True)
    rear_wing = models.FloatField(blank=True)
    sidepod = models.FloatField(blank=True)
    suspension = models.FloatField(blank=True)
    wheel_front = models.FloatField(blank=True)
    wheel_rear = models.FloatField(blank=True)
    total = models.FloatField(blank=True)


class Chassis(models.Model):
    body = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, related_name='b')
    front_wing = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, related_name='fw')
    rear_wing = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, related_name='rw')
    sidepod = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, related_name='s')
    suspension = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, related_name='su')
    wheel_front = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, related_name='wf')
    wheel_rear = models.ForeignKey(Part, on_delete=models.CASCADE, blank=True, related_name='wr')


class Simulation(models.Model):
    main_v = models.CharField(max_length=10)
    sub_v = models.IntegerField()
    slug = models.SlugField(primary_key=True)  # TODO - two different primary keys? Is composite necessary or will this do the trick?

    df = models.ForeignKey(Force, on_delete=models.CASCADE, blank=True, related_name='df')
    drag = models.ForeignKey(Force, on_delete=models.CASCADE, blank=True, related_name='drag')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True)
    chassis = models.ForeignKey(Chassis, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.main_v + '_' + str(self.sub_v)


    class Meta:
        db_table = 'Simulation'
        ordering = ['main_v', 'sub_v']

        managed = False
        # This requires manual creation(and updates probably) of the table
        '''
        sqlite3  db.sqlite3
        
        CREATE TABLE Simulation (
        main_v, 
        sub_v, 
        slug,
        df_id,
        drag_id,
        parent_id,
        chassis_id, 
        PRIMARY KEY (main_v, sub_v),
        FOREIGN KEY (df_id) REFERENCES mastersheet_force(id),
        FOREIGN KEY (drag_id) REFERENCES mastersheet_force(id),
        FOREIGN KEY (main_v, sub_v) REFERENCES Simulation(main_v, sub_v),
        FOREIGN KEY (chassis_id) REFERENCES mastersheet_chassis(id)
        );
        '''
