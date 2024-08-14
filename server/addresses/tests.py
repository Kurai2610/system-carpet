from django.test import TestCase
from graphene.test import Client
from core.schema import schema
from core.utils import decode_relay_id
from .models import (
    Locality,
    Neighborhood,
    Address
)


class AddressSchemaTests(TestCase):
    def setUp(self):
        self.client = Client(schema)
        self.locality = Locality.objects.create(name="Test Locality")
        self.neighborhood = Neighborhood.objects.create(
            name="Test Neighborhood", locality=self.locality)

    def test_create_address_mutation(self):
        mutation = '''
        mutation CreateAddress($details: String!, $neighborhoodId: ID!) {
            createAddress(details: $details, neighborhoodId: $neighborhoodId) {
                address {
                    id
                    details
                    neighborhood {
                        id
                        name
                    }
                }
            }
        }
        '''
        variables = {
            "details": "123 Test St",
            "neighborhoodId": self.neighborhood.id
        }
        response = self.client.execute(mutation, variables=variables)
        self.assertIsNone(response.get('errors'))

        data = response.get('data')
        address = data.get('createAddress').get('address')
        self.assertEqual(address['details'], variables['details'])
        _, neighborhood_id = decode_relay_id(address['neighborhood']['id'])
        self.assertEqual(neighborhood_id,
                         str(self.neighborhood.id))
        _, address_id = decode_relay_id(address['id'])
        db_address = Address.objects.get(id=address_id)
        self.assertEqual(db_address.details, variables['details'])
        self.assertEqual(db_address.neighborhood, self.neighborhood)

    def test_create_neighborhood_mutation(self):
        mutation = '''
        mutation CreateNeighborhood($name: String!, $localityId: ID!) {
            createNeighborhood(name: $name, localityId: $localityId) {
                neighborhood {
                    id
                    name
                    locality {
                        id
                        name
                    }
                }
            }
        }
        '''
        variables = {
            "name": "New Neighborhood",
            "localityId": self.locality.id
        }
        response = self.client.execute(mutation, variables=variables)
        self.assertIsNone(response.get('errors'))
        data = response.get('data')
        neighborhood = data.get('createNeighborhood').get('neighborhood')
        self.assertEqual(neighborhood['name'], variables['name'])
        _, locality_id = decode_relay_id(neighborhood['locality']['id'])
        self.assertEqual(locality_id, str(self.locality.id))
        _, neighborhood_id = decode_relay_id(neighborhood['id'])

        db_neighborhood = Neighborhood.objects.get(id=neighborhood_id)
        self.assertEqual(db_neighborhood.name, variables['name'])
        self.assertEqual(db_neighborhood.locality, self.locality)

    def test_create_locality_mutation(self):
        mutation = '''
        mutation CreateLocality($name: String!) {
            createLocality(name: $name) {
                locality {
                    id
                    name
                }
            }
        }
        '''
        variables = {
            "name": "New Locality"
        }
        response = self.client.execute(mutation, variables=variables)
        self.assertIsNone(response.get('errors'))
        data = response.get('data')
        locality = data.get('createLocality').get('locality')
        self.assertEqual(locality['name'], variables['name'])
        _, locality_id = decode_relay_id(locality['id'])

        db_locality = Locality.objects.get(id=locality_id)
        self.assertEqual(db_locality.name, variables['name'])
