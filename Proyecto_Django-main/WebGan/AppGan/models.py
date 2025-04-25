from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class LotsCattle(models.Model):
    lot_name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=255)
    ability = models.BigIntegerField()
    creation_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.lot_name

class Animals(models.Model):
    code_number = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    birth_date = models.DateField()
    weight = models.FloatField()
    father_bull = models.CharField(max_length=255, null=True, blank=True)
    lot = models.ForeignKey(LotsCattle, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Vaccines(models.Model):
    name = models.CharField(max_length=255)
    application_date = models.DateField()
    state = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AnimalVaccines(models.Model):
    vaccine = models.ForeignKey(Vaccines, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animals, on_delete=models.CASCADE)
    date_application = models.DateField()
    dose = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.animal.name} - {self.vaccine.name}"
