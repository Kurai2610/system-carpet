from django.test import TestCase
from graphene.test import Client
from core.schema import schema
from .models import (
    Locality,
    Neighborhood
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
