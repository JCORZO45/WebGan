from django.contrib import admin
from .models import LotsCattle, Animals, Vaccines, AnimalVaccines

admin.site.register(LotsCattle)
admin.site.register(Animals)
admin.site.register(Vaccines)
admin.site.register(AnimalVaccines)
