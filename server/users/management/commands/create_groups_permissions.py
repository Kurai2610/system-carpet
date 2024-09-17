from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create groups and assign permissions'

    def handle(self, *args, **options):
        groups = {
            'Admin': [],
            'Inventory Manager': [
                {
                    'app_label': 'inventories',
                    'models': ['inventoryitem'],
                    'actions': ['view', 'add', 'change', 'delete'],
                },
                {
                    'app_label': 'products',
                    'models': ['cartype', 'carmake', 'carmodel', 'productcategory', 'carpet'],
                    'actions': ['view', 'add', 'change', 'delete'],
                },
                {
                    'app_label': 'supply_chains',
                    'models': ['supplier', 'materialbysupplier', 'materialorder', 'orderdetail'],
                    'actions': ['view', 'add', 'change', 'delete'],
                },
            ],
            'Production Manager': [
                {
                    'app_label': 'addresses',
                    'models': ['locality', 'neighborhood', 'address'],
                    'actions': ['view', 'add', 'change', 'delete'],
                },
                {
                    'app_label': 'supply_chains',
                    'models': ['supplier', 'materialbysupplier', 'materialorder', 'orderdetail'],
                    'actions': ['view', 'add', 'change', 'delete'],
                },
            ],
            'Sales Assistant': [
                {
                    'app_label': 'sales',
                    'models': ['sale', 'saledetail', 'saledetailoption'],
                    'actions': ['view', 'add', 'change', 'delete'],
                }
            ],
            'Client': [
                {
                    'app_label': 'addresses',
                    'models': ['address'],
                    'actions': ['add', 'change'],
                },
                {
                    'app_label': 'addresses',
                    'models': ['locality', 'neighborhood'],
                    'actions': ['view'],
                },
                {
                    'app_label': 'shopping_carts',
                    'models': ['shoppingcart', 'shoppingcartitem', 'shoppingcartitemoption'],
                    'actions': ['view', 'add', 'change', 'delete'],
                },
                {
                    'app_label': 'sales',
                    'models': ['paymethod', 'deliverymethod', 'sale', 'saledetail', 'saledetailoption'],
                    'actions': ['view', 'add', 'change', 'delete'],
                },
            ],
        }

        admin_group, created = Group.objects.get_or_create(name='Admin')
        all_permissions = Permission.objects.all()
        admin_group.permissions.set(all_permissions)
        self.stdout.write(self.style.SUCCESS(
            'Assigned all permissions to Admin group'))

        for group_name, apps in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Created group: {group_name}'))

            perm_objects = []
            for app in apps:
                app_label = app['app_label']
                for model_name in app['models']:
                    for action in app['actions']:
                        perm_codename = f'{action}_{model_name}'
                        try:
                            perm = Permission.objects.get(
                                content_type__app_label=app_label,
                                content_type__model=model_name,
                                codename=perm_codename
                            )
                            perm_objects.append(perm)
                        except Permission.DoesNotExist:
                            self.stdout.write(self.style.WARNING(
                                f'Permission "{perm_codename}" does not exist for model "{model_name}" in app "{app_label}".'))

            group.permissions.add(*perm_objects)
            self.stdout.write(self.style.SUCCESS(
                f'Assigned permissions to group: {group_name}'))

        for group in Group.objects.all():
            self.stdout.write(self.style.SUCCESS(f'Group: {group.name}'))
            for perm in group.permissions.all():
                self.stdout.write(self.style.SUCCESS(
                    f'  Permission: {perm.codename}'))
