from django.core.exceptions import ValidationError
from models import InventoryItem


def validate_material_is_raw(value):
    try:
        inventory_item = InventoryItem.objects.get(id=value.id)
        if inventory_item.type != 'RAW':
            raise ValidationError(
                'El material asociado debe tener el tipo RAW.')
    except InventoryItem.DoesNotExist:
        raise ValidationError('El material asociado no existe.')
