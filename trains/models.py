from django.db import models


class TrainType(models.Model):
    class ServicesChooseField(models.TextChoices):
        air_conditioning = "air-conditioning"
        wc = "WC"
        bistro_carriage = "bistro carriage"
        wifi = "WIFI"
        sockets = "230V electrical sockets"
        information_system = "audio and visual information system"
        refreshment_service = "a in-seat refreshment service"

    name = models.CharField(max_length=255)
    services = models.CharField(max_length=255, choices=ServicesChooseField)


class Train(models.Model):
    name = models.CharField(max_length=255)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(TrainType, on_delete=models.CASCADE)
