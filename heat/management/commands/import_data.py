import pandas as pd
from django.core.management.base import BaseCommand
from heat.models import ThermalIsolation, Material, TypeLayer
import pandas as pd

# run import data: python manage.py import_data

excel_file = './heat/management/data/data_polystyrene.csv'
df = pd.read_csv(excel_file)


class Command(BaseCommand):
    help = 'Import data into the database'

    def handle(self, *args, **options):
        type_layer, created = TypeLayer.objects.get_or_create(type_layer='ocieplenie')
        for index, row in df.iterrows():
            name_layer, created = Material.objects.get_or_create(
                name_layer=row['name_layer'],
                defaults={'type_layer': type_layer}
            )

            ThermalIsolation.objects.create(
                name_layer=name_layer,
                thickness=row['thickness'],
                thermal_conductivity=row['thermal_conductivity'],
                cost=row['cost'],
                package_square_meters=row['package_square_meters']
            )
