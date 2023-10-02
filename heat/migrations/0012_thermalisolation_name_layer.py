# Generated by Django 4.2.4 on 2023-09-30 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('heat', '0011_remove_thermalisolation_name_layer'),
    ]

    operations = [
        migrations.AddField(
            model_name='thermalisolation',
            name='name_layer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='heat.material'),
        ),
    ]
