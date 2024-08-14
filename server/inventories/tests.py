from django.test import TestCase
from graphene.test import Client
from core.schema import schema
from core.utils import decode_relay_id
from .models import InventoryItem


class InventorySchemaTests(TestCase):
    def setUp(self):
        self.client = Client(schema)

    def test_create_inventory_item(self):
        mutation = '''
        mutation CreateInventoryItem($name: String!, $stock: Int!, $type: String!, $description: String!) {
            createInventoryItem(name: $name, stock: $stock, type: $type, description: $description) {
                inventoryItem {
                    id
                    name
                    stock
                    type
                    description
                }
            }
        }
        '''
        variables = {
            "name": "Test Item",
            "stock": 10,
            "type": "MAT",
            "description": "Test Description"
        }
        response = self.client.execute(mutation, variables=variables)
        self.assertIsNone(response.get('errors'))

        data = response.get('data')
        item = data.get('createInventoryItem').get('inventoryItem')
        self.assertEqual(item['name'], variables['name'])
        if variables['type'] == "MAT":
            self.assertEqual(item['type'], "Tapete")
        elif variables['type'] == "CUS":
            self.assertEqual(item['type'], "Orden Personalizada")
        elif variables['type'] == "RAW":
            self.assertEqual(item['type'], "Materia Prima")
        self.assertEqual(item['stock'], variables['stock'])
        self.assertEqual(item['description'], variables['description'])

        _, item_id = decode_relay_id(item['id'])
        db_item = InventoryItem.objects.get(id=item_id)
        self.assertEqual(db_item.name, variables['name'])
        self.assertEqual(db_item.stock, variables['stock'])
        self.assertEqual(db_item.type, variables['type'])
        self.assertEqual(db_item.description, variables['description'])
