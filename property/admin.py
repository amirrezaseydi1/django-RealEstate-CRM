from django.contrib import admin,messages
from django.contrib import admin
from .models import *

from django.contrib import admin
from .models import Province, City, District ,PropertyListing


class CityInline(admin.TabularInline):
    model = City
    extra = 1


class DistrictInline(admin.TabularInline):
    model = District
    extra = 1


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [CityInline]


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')
    list_filter = ('province',)
    search_fields = ('name',)
    inlines = [DistrictInline]


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    list_filter = ('city',)
    search_fields = ('name',)

class PropertyCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
class PropertyListingAdmin(admin.ModelAdmin):
    list_display = ('title','district','updated_at')
    list_filter = ('district',)








# admin.site.register(CuostomerRequest, CustomerRequestAdmin)


admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(PropertyCategory ,PropertyCategoryAdmin)
admin.site.register(Amenity ,AmenityAdmin)
admin.site.register(PropertyListing , PropertyListingAdmin)
# admin.site.register(CuostomerRequest,CuostomerRequestAdmin)
# admin.site.register(Costomer,CostomerAdminInline)


