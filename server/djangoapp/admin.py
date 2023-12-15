from django.contrib import admin
from .models import CarMake, CarModel

# Register your models here
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Number of extra CarModel forms to display

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

admin.site.register(CarModel) 
# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
