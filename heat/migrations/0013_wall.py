# Generated by Django 4.2.4 on 2023-10-02 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('heat', '0012_thermalisolation_name_layer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thickness', models.FloatField()),
                ('thermal_conductivity', models.FloatField()),
                ('cost', models.FloatField()),
                ('name_layer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='heat.material')),
            ],
        ),
    ]
