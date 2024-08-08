import re
from django.core.exceptions import ValidationError


def normalize_name(name, min_length=2, max_length=100):
    name = name.strip()

    name = re.sub(r'[^a-zA-Z\s\'\-]', '', name)

    if not name:
        raise ValidationError(
            'The name cannot be empty or contain only invalid characters.',
            code='invalid',
            params={'field': 'name'}
        )

    normalized_name = ' '.join(word.capitalize() for word in name.split())

    name_length = len(normalized_name)
    if name_length < min_length or name_length > max_length:
        raise ValidationError(
            f'The name must have between {min_length} and {
                max_length} characters. Current length: {name_length}',
            code='invalid_length',
            params={'field': 'name'}
        )

    return normalized_name
