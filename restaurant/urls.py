from django.urls import path, include
from rest_framework import routers

from restaurant.views import (
    RestaurantViewSet,
    MenuView,
    EmployeeViewSet,
    PositionViewSet,
    EmployeeScoreView,
    current_day_menu,
)

router = routers.DefaultRouter()

router.register("restaurants", RestaurantViewSet)
router.register("position", PositionViewSet)
router.register("user", EmployeeViewSet)
router.register("score", EmployeeScoreView, basename="employee_score")

urlpatterns = [
    path("", include(router.urls)),
    path("menu/", MenuView.as_view(), name="menu"),
    path("today_menu/", current_day_menu, name="today-menu"),
]

app_name = "restaurant"
