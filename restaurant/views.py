import datetime

from django.contrib.auth.hashers import make_password
from rest_framework import mixins, viewsets, status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from restaurant.models import Restaurant, Menu, Employee, Position, EmployeeScore
from restaurant.serializer import (
    RestaurantSerializer,
    MenuSerializer,
    EmployeeSerializer,
    PositionSerializer,
    EmployeeScoreSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuView(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


@api_view(["GET"])
def current_day_menu(request):
    today = datetime.date.today()
    menu = Menu.objects.filter(date=today)
    serializer = MenuSerializer(menu, many=True)
    return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        queryset = Employee.objects.filter(id=self.request.user.id)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        password = data.pop("password", None)[0]
        data["password"] = make_password(password, salt=None, hasher="default")
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return Response(
                {"error": "You can only update your own profile."},
                status=status.HTTP_403_FORBIDDEN,
            )
        data = request.data.copy()
        password = data.pop("password", None)
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()
        return Response(serializer.data)


class PositionViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        current_date = datetime.date.today()
        data = request.POST.copy()

        today_menu = Menu.objects.filter(
            date=current_date, restaurant=data["restaurant"]
        )

        if len(today_menu) == 0:
            today_menu = Menu.objects.create(
                restaurant=Restaurant.objects.get(id=data["restaurant"])
            )
        else:
            today_menu = today_menu.first()

        data["menu"] = today_menu

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save(menu=today_menu)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class EmployeeScoreView(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = EmployeeScore.objects.all()
    serializer_class = EmployeeScoreSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(employee=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.POST.copy()
        data["employee"] = request.user.id

        EmployeeScore.objects.filter(
            employee=data["employee"], menu=data["menu"]
        ).delete()

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        employee = Employee.objects.get(id=request.user.id)

        serializer.save(employee=employee)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
