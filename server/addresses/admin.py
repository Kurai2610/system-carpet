from django.contrib import admin
from .models import Address, Locality, Neighborhood

# Register your models here.

admin.site.register(Address)
admin.site.register(Locality)
admin.site.register(Neighborhood)
