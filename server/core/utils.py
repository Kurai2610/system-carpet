import re
from core.errors import ValidationError

def normalize_name(name, min_length=1, max_length=100):
    name = name.strip()

    name = re.sub(r'[^a-zA-Z\s\'\-]', '', name)

    if not name:
        raise ValidationError('El nombre no puede estar vacío o contener solo caracteres inválidos.', field='name')

    normalized_name = ' '.join(word.capitalize() for word in name.split())
    
    name_length = len(normalized_name)
    if name_length < min_length or name_length > max_length:
        raise ValidationError(f'El nombre debe tener entre {min_length} y {max_length} caracteres. Longitud actual: {name_length}', field='name')
    
    return normalized_name