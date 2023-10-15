from django.contrib import admin
from .models import Location, RentalInformation, HostelInformation

admin.site.register(Location)
admin.site.register(RentalInformation)
admin.site.register(HostelInformation)
