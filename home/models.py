from django.db import models


# Create your models here.

class Banner(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='عنوان'
    )

    subtitle = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='زیرعنوان'
    )

    image = models.ImageField(
        upload_to='banners/',
        verbose_name='تصویر بنر'
    )

    login_url = models.CharField(
        max_length=300,
        default='/login/',
        verbose_name='لینک ورود به سایت'
    )

    about_url = models.CharField(
        max_length=300,
        default='/about/',
        verbose_name='لینک معرفی سایت'
    )

    cities_url = models.CharField(
        max_length=300,
        default='/cities/',
        verbose_name='لینک جستجوی ملک در شهرها'
    )

    properties_url = models.CharField(
        max_length=300,
        default='/properties/',
        verbose_name='لینک ورود به بخش املاک'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد',null=True,blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ بروزرسانی',null=True,blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنرها'
        ordering = ['-created_at']
class QuickLink(models.Model):
    title = models.CharField(max_length=100,verbose_name='عنوان لینک')
    url = models.CharField(max_length=300,verbose_name='آدرس (url)',help_text="مثال: /properties/search/ یا آدرس کامل اینترنتی")
    order = models.PositiveIntegerField(        default=0,
        verbose_name="ترتیب نمایش",
        help_text="هرچه عدد کمتر باشد، لینک جلوتر نمایش داده می‌شود."
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "لینک سریع"
        verbose_name_plural = "لینک‌های سریع"

    def __str__(self):
        return self.title
