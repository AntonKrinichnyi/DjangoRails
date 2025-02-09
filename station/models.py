from django.db import models


class TrainType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return f"{self.name}"


class Train(models.Model):
    name = models.CharField(max_length=255, unique=True)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(TrainType, on_delete=models.CASCADE)
    
    @property
    def capacity(self) -> int:
        return self.cargo_num * self.places_in_cargo
    
    def __str__(self) -> str:
        return f"{self.name}"


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.full_name()
