import base64
import re
from django.core.exceptions import ValidationError


def normalize_name(name, min_length=2, max_length=50, numbers=False):
    name = name.strip()

    if not numbers:
        pattern = r'[^a-zA-Z\s\'\-áéíóúÁÉÍÓÚ]'
    else:
        pattern = r'[^a-zA-Z0-9\s\'\-áéíóúÁÉÍÓÚ]'

    if re.search(pattern, name):
        raise ValidationError('The name contains invalid characters.')

    if not name:
        raise ValidationError(
            'The name cannot be empty or contain only invalid characters.')

    normalized_name = ' '.join(word.capitalize() for word in name.split())

    name_length = len(normalized_name)
    if name_length < min_length or name_length > max_length:
        raise ValidationError(
            f'The name must have between {min_length} and {max_length} characters. Current length: {name_length}')

    return normalized_name


def normalize_password(password, min_length=8, max_length=20):
    password = password.strip()

    if not password:
        raise ValidationError('The password cannot be empty.')

    password_length = len(password)
    if password_length < min_length or password_length > max_length:
        raise ValidationError(
            f'The password must have between {min_length} and {max_length} characters. Current length: {password_length}')

    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])(?=.*\d)[A-Za-z\d@$!%*?&#]{8,}$', password):
        raise ValidationError(
            'The password must contain at least one digit, one uppercase letter, one lowercase letter, one special character (@, $, !, %, *, ?, &, #), and be at least 8 characters long.')

    return password


def decode_relay_id(global_id):
    decoded_bytes = base64.b64decode(global_id)
    decoded_str = decoded_bytes.decode('utf-8')
    type_name, id_str = decoded_str.split(':')
    return type_name, id_str
