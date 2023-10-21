from django.test import TestCase

from .models import TypeLayer


# Create your tests here.

class TypeLayerTestCase(TestCase):
    def test_type_layer_creation(self):
        # Create a TypeLayer instance
        type_layer = TypeLayer.objects.create(type_layer="mur")

        # Check if the instance was created successfully
        self.assertEqual(type_layer.type_layer, "mur")

    def test_unique_constraint(self):
        # Create a TypeLayer instance with a unique value
        unique_type_layer = TypeLayer(type_layer="mur")
        unique_type_layer.save()

        # Try to create another instance with the same value, which should raise an IntegrityError
        with self.assertRaises(Exception):
            duplicate_type_layer = TypeLayer(type_layer="mur")
            duplicate_type_layer.save()
