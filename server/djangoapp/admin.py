from django.contrib import admin
from .models import CarModel, CarMake


class CarModelInLine(admin.StackedInline):
    model = CarModel


class CarModelAdmin(admin.ModelAdmin):
    ...


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInLine]
    list_display = ["name"]


admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
