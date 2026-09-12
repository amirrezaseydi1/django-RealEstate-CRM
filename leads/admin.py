from django.contrib import admin

from leads.models import *

class CustomerRequestInline(admin.TabularInline):
    model = CuostomerRequest
    extra = 1

# Register your models here.
@admin.register(Costomer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at')
    inlines = [CustomerRequestInline]

@admin.register(CuostomerRequest)
class CustomerRequestAdmin(admin.ModelAdmin):
    list_display = ('id','customer', 'title', 'show_districts','created_at')

    def show_districts(self,obj):
        return "، ".join([district.name for district in obj.district.all()])
    show_districts.short_description = "محله‌ها"



# مشاور: فقط خودش ثبت شود
# مدیر/ادمین: بتواند برای دیگران هم task بسازد
@admin.register(AgentTask)
class AgentTaskAdmin(admin.ModelAdmin):
    list_display = ('id','title','agent','priority')
    readonly_fields = ('agent','created_at','updated_at','completed_at','sms_sent','sms_sent_as')
    fields = (
        'agent',
        'title',
        'description',
        'task_type',
        'priority',
        'status',
        'due_date',
        'due_time',
        'related_customer',
        'related_request',
        'related_property',
        'is_auto_created',
        'sms_reminder_enabled',
        'sms_sent',
        'sms_sent_as',
        'completed_at',
        'created_at',
        'updated_at',
    )










