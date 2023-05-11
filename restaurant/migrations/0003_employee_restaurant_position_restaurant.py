# Generated by Django 4.2.1 on 2023-05-11 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("restaurant", "0002_alter_employee_position"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="restaurant_employee",
                to="restaurant.restaurant",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="position",
            name="restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="restaurant_position",
                to="restaurant.restaurant",
            ),
            preserve_default=False,
        ),
    ]
