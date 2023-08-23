# Generated by Django 4.2.4 on 2023-08-23 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TypeLayer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type_layer", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="BuildingPartition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name_layer", models.CharField(max_length=100)),
                ("thickness", models.FloatField()),
                ("thermal_conductivity", models.FloatField()),
                ("cost", models.FloatField()),
                (
                    "type_layer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="heat.typelayer"
                    ),
                ),
            ],
        ),
    ]
