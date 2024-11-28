from django.db import models


class Orendsrs(models.Model):
    name_firm = models.CharField(max_length=255)
    boss = models.CharField(max_length=255)
    number_phone = models.CharField(max_length=15)


class Rooms(models.Model):
    area = models.FloatField()
    cost_area_one_m = models.FloatField()
    floor = models.IntegerField()
    floor_phone = models.BooleanField()
    decoration_floor = models.CharField(max_length=10, choices=[('normal', 'Normal'), ('good', 'Good'), ('euro', 'Euro')])


class Renta(models.Model):
    date_start = models.DateField()
    count_days = models.PositiveIntegerField()
    goal_rental = models.CharField(max_length=10, choices=[('office', 'Office'), ('kiosk', 'Kiosk'), ('warehouse', 'Warehouse')])
    id_orendsrs = models.ForeignKey(Orendsrs, on_delete=models.CASCADE)
    id_number_rooms = models.ForeignKey(Rooms, on_delete=models.CASCADE)
