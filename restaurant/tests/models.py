import datetime

from django.db import IntegrityError
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from restaurant.models import Restaurant, Menu, Position, Employee, EmployeeScore


def get_restaurant():
    return Restaurant.objects.create(name="test_name")


def get_menu(restaurant):
    return Menu.objects.create(restaurant=restaurant)


class RestaurantTests(TestCase):
    def setUp(self):
        self.restaurant = get_restaurant()

    def test_correct_str(self):
        self.assertEqual(str(self.restaurant), "test_name")


class MenuTests(TestCase):
    def setUp(self):
        self.restaurant = get_restaurant()
        self.menu = get_menu(self.restaurant)

    def test_date_add_automatically(self):
        self.assertEqual(self.menu.date, datetime.date.today())

    def test_correct_str(self):
        self.assertEqual(
            str(self.menu),
            f"{self.restaurant.name} - {datetime.date.today()}"
        )


class PositionTests(TestCase):
    def setUp(self):
        self.restaurant = get_restaurant()
        self.menu = get_menu(self.restaurant)

        self.position = Position.objects.create(
            name="test_name",
            price=55,
            menu=self.menu,
            restaurant=self.restaurant
        )

    def test_correct_str(self):
        self.assertEqual(
            str(self.position),
            f"{self.position.name} - {self.position.price}"
        )


class EmployeeScoreTests(TestCase):
    def setUp(self):
        self.restaurant = get_restaurant()

        self.menu = get_menu(self.restaurant)
        self.employee = Employee.objects.create(
            username="test_username",
            email="test_email",
            password="test_password",
            restaurant=self.restaurant
        )

    def test_employee_and_menu_are_unique(self):
        with self.assertRaises(IntegrityError):
            EmployeeScore.objects.create(
                employee=self.employee,
                menu=self.menu,
                points=5
            )

            EmployeeScore.objects.create(
                employee=self.employee,
                menu=self.menu,
                points=8
            )
