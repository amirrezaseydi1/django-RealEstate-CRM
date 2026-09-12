from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile

# ۱. تعریف پروفایل به عنوان یک فرم داخلی (Inline)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'اطلاعات پروفایل'
    fields = ['role', 'phone', 'address']

# ۲. ساخت یک ادمین شخصی‌سازی شده برای کاربر
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username','email','get_role','is_staff','is_superuser')
    list_filter = ('is_staff','is_superuser','profile__role')

    def get_role(self, obj):
        return obj.profile.get_role_display()
    get_role.short_description = 'نقش'


# ۳. لغو ثبت ادمین پیش‌فرض و ثبت ادمین جدید ما
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
