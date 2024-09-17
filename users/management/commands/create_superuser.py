from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a superuser with default values'

    def handle(self, *args, **kwargs):
        email = "admin@admin.com"
        phone = "1234567890"
        first_name = "Admin"
        last_name = "Default"
        password = "INSECURE_PASSWORD!1a"

        User = get_user_model()

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(
                'User with this email already exists'))
        else:
            User.objects.create_superuser(
                email=email,
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(
                f'Superuser with email "{email}" created successfully'))
