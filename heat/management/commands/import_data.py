from django.core.management.base import BaseCommand
from heat.models import Polystyrene
import csv


class Command(BaseCommand):
    help = 'Import data into the database'

    def handle(self, *args, **options):
        with open('./heat/management/data/data_polystyrene.csv', 'r', encoding='iso-8859-2') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name_polystyrene, thermal_conductivity, thickness, cost = [cell.encode('iso-8859-2').decode('utf-8') for
                                                                           cell in row]
                Polystyrene.objects.create(name_polystyrene=name_polystyrene, thickness=thickness,
                                           thermal_conductivity=thermal_conductivity, cost=cost)
