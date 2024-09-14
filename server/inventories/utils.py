from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from core.utils import normalize_name
from .models import InventoryItem


def create_inventory_item(name, stock, type, description=None):
    try:
        name = normalize_name(name)
        if description:
            description = description.strip()
        inventory_item = InventoryItem(
            name=name, description=description, stock=stock, type=type)
        inventory_item.save()
        return inventory_item
    except ValidationError as e:
        raise ValueError(e)
    except IntegrityError:
        raise ValueError("Inventory item already exists")
    except Exception as e:
        raise ValueError(f"Unknown Error: {str(e)}")


def delete_inventory_item(id):
    try:
        inventory_item = InventoryItem.objects.get(pk=id)
        inventory_item.delete()
        return True
    except InventoryItem.DoesNotExist:
        raise ValueError("Item not found")
    except Exception as e:
        raise ValueError(f"Unknown Error: {str(e)}")


def update_inventory_item(id, name=None, description=None, stock=None, type=None):
    if not name and not description and stock is None and not type:
        raise ValueError("At least one field is required")

    try:
        inventory_item = InventoryItem.objects.get(pk=id)
        if name:
            name = normalize_name(name)
            inventory_item.name = name
        if description:
            description = description.strip()
            inventory_item.description = description
        if stock is not None:
            if stock >= 0:
                inventory_item.stock = stock
            else:
                raise ValueError("Stock must be a positive integer")
        if type:
            inventory_item.type = type

        inventory_item.save()
        return inventory_item
    except InventoryItem.DoesNotExist:
        raise ValueError("Item not found")
    except IntegrityError:
        raise ValueError("Inventory item already exists")
    except ValidationError as e:
        raise ValueError(e)
    except Exception as e:
        raise ValueError(f"Unknown Error: {str(e)}")
