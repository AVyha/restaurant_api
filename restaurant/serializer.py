from rest_framework import serializers

from restaurant.models import Restaurant, Menu, Employee, Position, EmployeeScore


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["name"]


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["name", "price", "menu", "restaurant"]
        read_only_fields = ["menu"]


class PositionForMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["name", "price"]


class MenuSerializer(serializers.ModelSerializer):
    average_score = serializers.SerializerMethodField()
    menu_position = PositionForMenuSerializer(many=True)
    restaurant = RestaurantSerializer(many=False)

    class Meta:
        model = Menu
        fields = ["restaurant", "date", "menu_position", "average_score"]
        read_only_fields = ["date", "menu_position"]

    def get_average_score(self, obj):
        scores = obj.employee_score.values_list("points", flat=True)
        if scores:
            return sum(scores) / len(scores)
        else:
            return None


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["username", "email", "password", "first_name", "last_name", "restaurant"]


class EmployeeScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeScore
        fields = ["employee", "menu", "points"]
        read_only_fields = ["employee"]
