from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError


# Create your models here.
# مدل‌های سلسله‌مراتبی مکان (استان > شهر > محله)
class Province(models.Model):
    name = models.CharField(max_length=100, verbose_name='استان')

    class Meta:
        verbose_name = 'استان'
        verbose_name_plural = 'استان'

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities', verbose_name='ایتان')
    name = models.CharField(max_length=100, verbose_name='شهر')

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهر'

    def __str__(self):
        return self.name


class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts', verbose_name='شهر')
    name = models.CharField(max_length=100, verbose_name='محله')

    class Meta:
        verbose_name = 'محله'
        verbose_name_plural = 'محله ها'

    def __str__(self):
        return self.name


# karbari (vila apartman land shop)
class PropertyCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='نوع کاربری ملک')

    class Meta:
        verbose_name = 'کاربری ملک'
        verbose_name_plural = 'کاربری های ملک'

    def __str__(self):
        return self.name


# امکانات مثل پارکینگ آسانسور
class Amenity(models.Model):
    name = models.CharField(max_length=50, verbose_name='امکانات')

    class Meta:
        verbose_name = 'امکانات'
        verbose_name_plural = 'امکانات'

    def __str__(self):
        return self.name



class PropertyListing(models.Model):
    class DealType(models.TextChoices):
        SALE_PROPERTY = 'SALE_PROPERTY', 'فروش مسکونی'
        SALE_BUSINESS = 'SALE_BUSINESS', 'فروش اداری تجاری'
        RENT_PROPERTY = 'RENT_PROPERTY', 'رهن و اجاره مسکونی'
        RENT_BUSINESS = 'RENT_BUSINESS', 'رهن و اجاره اداری نجاری'

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'پیش نویس'
        AVAILABLE = "AVAILABLE", "انتشار یافته"
        SOLD_OR_RENT = "SOLD", "واگذار شده"

    # موقعیت ملک
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True, verbose_name='محله')

    # اطلاعات ملک
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name='عنوان آگهی')
    slug = models.SlugField(unique=True, max_length=200, null=True, blank=True, allow_unicode=True,
                            verbose_name='اسلاگ')
    description = RichTextField(max_length=500, null=True, blank=True, verbose_name='توضیحات ملک')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name='وضعیت انتشار')

    # اطلاعات مالک
    owner_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام مالک /موجر')
    owner_phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='شماره تماس مالک')
    # کاربر
    agent = models.ForeignKey(User,on_delete=models.CASCADE,related_name='listing',verbose_name='مشاور ثبت کننده ')
    # دسته بندی ها
    deal_type = models.CharField(max_length=25, choices=DealType.choices, default=DealType.SALE_PROPERTY,
                                 verbose_name='نوع معامله')
    PROPERTY_TYPE = models.ForeignKey(PropertyCategory, null=True, blank=True, on_delete=models.CASCADE,
                                      related_name='listings', verbose_name='نوع ملک')

    # ... بقیه فیلدها (متراژ، خواب و ...) ...
    area = models.PositiveIntegerField(null=True, blank=True, verbose_name='متراژ(متر مربع)')
    year_built = models.PositiveIntegerField(blank=True, null=True, verbose_name='سال ساخت')
    rooms = models.PositiveIntegerField(default=1, verbose_name='تعداد اتاق')
    total_floors = models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد کل طبقات')
    # امکانات
    amenities = models.ManyToManyField(Amenity, blank=True, verbose_name='امکانات')

    # اطلاعات مالی
    selling_price = models.DecimalField(max_digits=15, decimal_places=0, null=True, blank=True,
                                        verbose_name='قیمت کل فروش')
    mortgage_price = models.PositiveIntegerField(null=True, blank=True, verbose_name='مبلغ رهن')
    rent_price = models.PositiveIntegerField(null=True, blank=True, verbose_name='اجاره ماهیانه')

    # tags and time
    tags = TaggableManager(blank=True, verbose_name='تگ ها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت انتشار')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'آگهی ملک'
        verbose_name_plural = "آگهی های املاک"

    def __str__(self):
        return self.title or 'بدون عنوان'

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        # ذخیره اولیه برای تولید PK
        super().save(*args, **kwargs)

        # ساخت اسلاگ بعد از ایجاد PK
        if is_new and self.title and not self.slug:
            persian_slug = slugify(self.title, allow_unicode=True)
            self.slug = f"{self.pk}-{persian_slug}"
            super().save(update_fields=['slug'])


# مدل گالری تصاویر (رابطه یک به چند با آگهی)
class PropertyImage(models.Model):
    property = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='images',
                                 verbose_name='آگهی مرتبط')
    image = models.ImageField(upload_to='properties/galleries/%Y/%m', verbose_name='تصویر')
    is_cover = models.BooleanField(default=False, verbose_name='تصویر اصلی')

    def __str__(self):
        return f"تصویر مربوط به: {self.property.title}"



