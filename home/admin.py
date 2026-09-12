from django.contrib import admin
from .models import *
# Register your models here.
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title',)
@admin.register(QuickLink)
class QuickLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')  # امکان ویرایش سریع ترتیب و وضعیت فعال بودن بدون ورود به صفحه جزئیات
    list_filter = ('is_active',)
    search_fields = ('title', 'url')
admin.site.register(Banner,BannerAdmin)