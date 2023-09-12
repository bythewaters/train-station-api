from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class TrainType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    max_speed = models.IntegerField()
    services = models.ManyToManyField(
        Service, related_name="train_type", null=True
    )

    def __str__(self) -> str:
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=255)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(
        TrainType, on_delete=models.CASCADE, related_name="train", null=True
    )

    def __str__(self) -> str:
        return self.name
