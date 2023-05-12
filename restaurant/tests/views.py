from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from restaurant.models import Restaurant, Employee


class RestaurantViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_all_restaurants(self):
        Restaurant.objects.create(name="test1")
        Restaurant.objects.create(name="test2")

        response = self.client.get(
            reverse("restaurant:restaurant-list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_create_restaurant(self):
        response = self.client.post(
            reverse("restaurant:restaurant-list"),
            {
                "name": "testname"
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Restaurant.objects.count(), 1
        )


class EmployeeViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.restaurant = Restaurant.objects.create(name="test_name")

        self.data = {
            "username": "username_test",
            "email": "email_test@gmail.test",
            "password": "password_test",
            "first_name": "first_name_test",
            "last_name": "last_name_test",
            "restaurant": self.restaurant.pk
        }

    def test_create_employee(self):
        response = self.client.post(
            reverse("restaurant:employee-list"),
            self.data
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Employee.objects.count(), 1
        )
        self.assertNotEqual(
            response.data["password"],
            self.data["password"]
        )
