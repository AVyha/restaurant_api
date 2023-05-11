from django.contrib.auth.models import AbstractUser
from django.db import models

from restaurant.validator import validate_score


class Restaurant(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Menu(models.Model):
    date = models.DateField(auto_now_add=True)

    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, related_name="menu"
    )
    score = models.ManyToManyField(
        "Employee", through="EmployeeScore", related_name="employee_score"
    )

    def __str__(self):
        return f"{self.restaurant} - {self.date}"


class Employee(AbstractUser):
    SERVER = "SR"
    COOK = "CK"
    DISHWASHER = "DH"
    HOST_HOSTESS = "HH"
    MANAGER = "MG"
    BARTENDER = "BT"

    POSITION_CHOICES = (
        (SERVER, "Server"),
        (COOK, "Cook"),
        (DISHWASHER, "Dishwasher"),
        (HOST_HOSTESS, "Host/Hostess"),
        (MANAGER, "Manager"),
        (BARTENDER, "Bartender"),
    )

    position = models.CharField(max_length=2, choices=POSITION_CHOICES, default="CK")

    score = models.ManyToManyField(
        "Menu", through="EmployeeScore", related_name="menu_score"
    )
    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, related_name="restaurant_employee"
    )

    def __str__(self):
        return self.username


class EmployeeScore(models.Model):
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    menu = models.ForeignKey(
        "Menu", on_delete=models.CASCADE, related_name="employee_score"
    )
    points = models.IntegerField(validators=[validate_score])

    class Meta:
        unique_together = ["employee", "menu"]


class Position(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()

    menu = models.ForeignKey(
        "Menu", on_delete=models.CASCADE, related_name="menu_position"
    )
    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, related_name="restaurant_position"
    )

    def __str__(self):
        return f"{self.name} - {self.price}"
