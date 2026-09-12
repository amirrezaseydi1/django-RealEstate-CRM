from django import forms
from .models import *

class PropertyStep2Form(forms.ModelForm):
    class Meta:
        model = PropertyListing
        fields = [
            'title',
            'description',
            'PROPERTY_TYPE',
            'area',
            'year_built',
            'rooms',
            'total_floors',
            'amenities',
            'deal_type',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'مثال: آپارتمان ۱۲۰ متری نوساز در الهیه'}),
            'description': forms.Textarea(attrs={'placeholder': 'جزئیات بیشتر درباره ملک...'}),
            'property_type': forms.Select(attrs={'class': 'select2'}),  # اگر از select2 استفاده کردی
            'area': forms.NumberInput(attrs={'min': 1}),
            'year_built': forms.NumberInput(attrs={'min': 1800, 'max': 2025}),  # فرض کنید سال جاری 2025 است
            'rooms': forms.NumberInput({'min': 0}),
            'total_floors': forms.NumberInput({'min': 1}),
            'amenities': forms.CheckboxSelectMultiple,
            'deal_type': forms.Select,
        }
        # تنظیم verbose_name ها برای نمایش بهتر در فرم
        labels = {
            'title': 'عنوان آگهی',
            'description': 'توضیحات',
            'property_type': 'نوع ملک',
            'area': 'متراژ (مترمربع)',
            'year_built': 'سال ساخت',
            'rooms': 'تعداد اتاق خواب',
            'total_floors': 'تعداد طبقات کل ساختمان',
            'amenities': 'امکانات',
            'deal_type': 'نوع معامله',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # تنظیم فیلدهای ManyToMany برای نمایش صحیح
        if 'amenities' in self.fields:
            self.fields['amenities'].queryset = Amenity.objects.all()

class PropertyStep3Form(forms.ModelForm):
    class Meta:
        model = PropertyListing
        fields = ['owner_name', 'owner_phone', 'selling_price', 'mortgage_price', 'rent_price', ]
        labels = {
            'owner_name': 'نام مالک',
            'owner_phone': 'شماره تماس مالک',
            'selling_price': 'قیمت فروش',
            'mortgage_price': 'مبلغ رهن',
            'rent_price': 'مبلغ اجاره ماهانه (تومان)',
        }
        widgets = {
            'owner_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال علی رضایی'}),
            'owner_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'مثال09123456789'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مبلغ فروش'}),
            'mortgage_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مبلغ رهن'}),
            'rent_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مبلغ اجاره'}),
        }

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True
class PropertyImageForm(forms.ModelForm):
    # این خط بسیار مهم است: بازنویسی فیلد برای پشتیبانی از چند فایل
    image = forms.ImageField(
        label='تصویر ملک',
        widget=forms.FileInput(attrs={'class': 'form-control','accept': 'image/*'})
    )

    class Meta:
        model = PropertyImage
        fields = ['image']
        # بخش labels و widgets از اینجا حذف شد چون در بالا تعریف کردیم
