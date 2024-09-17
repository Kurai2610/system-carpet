from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from .models import (
    Address,
    Neighborhood,
)


def create_address(address_details, neighborhood_id):
    address = Address.objects.create(
        details=address_details,
        neighborhood_id=neighborhood_id
    )
    return address


def delete_address(address_id):
    address = Address.objects.get(id=address_id)
    address.delete()


def update_address(address_id, address_details=None, neighborhood_id=None):
    if not address_details and not neighborhood_id:
        raise ValueError("Details or Neighborhood is required")

    try:
        address = Address.objects.get(id=address_id)
        if address_details is not None:
            address_details = address_details.strip()
            address.details = address_details
        if neighborhood_id is not None:
            neighborhood_obj = Neighborhood.objects.get(id=neighborhood_id)
            address.neighborhood = neighborhood_obj
        address.save()
        return address
    except Address.DoesNotExist:
        raise ValueError("Address not found")
    except Neighborhood.DoesNotExist:
        raise ValueError("Neighborhood not found")
    except ValidationError as e:
        raise ValueError(e)
    except IntegrityError:
        raise ValueError("Address already exists")
    except Exception as e:
        raise ValueError(f"Unknown Error: {str(e)}")
