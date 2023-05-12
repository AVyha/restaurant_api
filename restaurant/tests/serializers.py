from django.test import TestCase

from restaurant.models import Restaurant, Position, Menu, Employee
from restaurant.serializer import RestaurantSerializer, PositionSerializer, EmployeeSerializer


def get_restaurant():
    return Restaurant.objects.create(name="test_name")


class RestaurantSerializerTests(TestCase):
    def setUp(self):
        self.data = {"name": "test_name"}

    def test_serializer_contains_expected_fields(self):
        self.serializer = RestaurantSerializer(data=self.data)
        self.serializer.is_valid()
        self.serializer.save()

        expect = ["name"]

        self.assertEqual(list(self.serializer.data.keys()), expect)

    def test_create(self):
        self.serializer = RestaurantSerializer(data=self.data)

        self.serializer.is_valid()
        restaurant = self.serializer.save()

        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(restaurant.name, "test_name")


class EmployeeSerializerTests(TestCase):
    def setUp(self):
        self.restaurant = get_restaurant()

        self.data = {
            "username": "username_test",
            "email": "email_test@gmail.test",
            "password": "password_test",
            "first_name": "first_name_test",
            "last_name": "last_name_test",
            "restaurant": self.restaurant.pk
        }

    def test_create(self):
        self.serializer = EmployeeSerializer(data=self.data)
        self.serializer.is_valid()
        employee = self.serializer.save()

        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(employee.username, "username_test")
        self.assertEqual(employee.email, "email_test@gmail.test")
