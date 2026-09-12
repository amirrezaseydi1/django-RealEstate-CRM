from django.db import models
from property .models import *
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils import timezone
# Create your models here.

class Costomer(models.Model):
    name =models.CharField(max_length=200,verbose_name='نام مشتری')
    phone =models.CharField(max_length=20,unique=True,verbose_name="شماره تلفن")
    description=models.CharField(max_length=1500,verbose_name="توضیحات")
    created_at =models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ایجاد")
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'مشتری'
        verbose_name_plural = 'لیست مشتریان'

class CuostomerRequest(models.Model):
    class RequestStatus(models.TextChoices):
        ACTIVE = "active", "فعال"
        IN_PROGRESS = "in_progress", "در حال پیگیری"
        CLOSED = "closed", "بسته شده"
        CANCELED = "canceled", "لغو شده"
    class DealType(models.TextChoices):
        SALE_PROPERTY = 'SALE_PROPERTY', 'فروش مسکونی'
        SALE_BUSINESS = 'SALE_BUSINESS', 'فروش اداری تجاری'
        RENT_PROPERTY = 'RENT_PROPERTY', 'رهن و اجاره مسکونی'
        RENT_BUSINESS = 'RENT_BUSINESS', 'رهن و اجاره اداری نجاری'
    title =models.CharField(max_length=300,null=True,blank=True,verbose_name="عناوان آگهی درخواست")
    customer = models.ForeignKey(Costomer,related_name='requests',on_delete=models.CASCADE)
    #نوع درخواست خرید یا اجاره
    dealtype =models.CharField(max_length=50,choices=DealType.choices,default=DealType.SALE_PROPERTY)
    property_type = models.ForeignKey(PropertyCategory,on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=RequestStatus.choices,default=RequestStatus.ACTIVE,verbose_name="وضعیت آگهی")
    district =models.ManyToManyField(District,verbose_name="انتخاب محله")
    min_area = models.IntegerField(null=True,blank=True,verbose_name="حداقل متراژ")
    max_area= models.IntegerField(null=True,blank=True,verbose_name="حداکثر متراژ")

    #اطلاعات مالی
    mortgage_price = models.PositiveIntegerField(null=True, blank=True, verbose_name='مبلغ رهن')
    rent_price = models.PositiveIntegerField(null=True, blank=True, verbose_name='اجاره ماهیانه')
    min_price = models.BigIntegerField(null=True, blank=True,verbose_name="حداقل قیمت")
    max_price = models.BigIntegerField(null=True, blank=True,verbose_name="حداکثر قیمت")
    rooms =models.IntegerField(null=True,blank=True)
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'درخواست ملک'
        verbose_name_plural = "درخواست های املاک"
    def __str__(self):
        return self.title or "بدون نام"
class RequestFollowUp(models.Model):
    customer = models.ForeignKey(Costomer,on_delete=models.CASCADE,related_name='followups',verbose_name="مشتری")
    request = models.ForeignKey(CuostomerRequest,on_delete=models.CASCADE,related_name='followup',null=True,blank=True,verbose_name="درخواست مرتبط")
    agent  =models.ForeignKey(User,on_delete=models.SET_NULL,null=True,verbose_name="مشاور ثبت کننده")
    note =RichTextField()
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ثبت")
    class Meta:
        ordering =['-created_at']

    def __str__(self):
        return f"پیگیری برای{self.name} در {self.created_at.strftime('%Y-%m-%d %H:%M')}"



class AgentTask(models.Model):
    TASK_TYPE_CHOICES = [
        ('call','تماس'),
        ('follow_up','پیگیری'),
        ('visit','بازدید'),
        ('send_file','ارسال فایل'),
        ('meeting','جلسه'),
        ('reminder','یادآوری'),
        ('custom','سفارشی'),
    ]
    PRIORITY_CHOICES = [
        ('low','پایین'),
        ('medium','متوسط'),
        ('high','زیاد'),
        ('urgent','فوری'),
    ]
    STATUS_CHOICES = [
        ('todo','درحال انجام'),
        ('done','لنجلم شده'),
        ('cancelled','لغو شده'),
        ('mised','انجام نشده'),
    ]
    agent = models.ForeignKey(User,on_delete=models.CASCADE,related_name='agents_tasks',verbose_name='مشاور')
    title = models.CharField(max_length=255,verbose_name="عنولن کار")
    description = RichTextField(null=True,blank=True,verbose_name='توضیحات')
    task_type = models.CharField(max_length=30,choices=TASK_TYPE_CHOICES,default='custom',verbose_name='نوع کار')
    priority =models.CharField(max_length=30,choices=PRIORITY_CHOICES,default='medium',verbose_name='اولویت')
    status =models.CharField(max_length=30,choices=STATUS_CHOICES,default='todo',verbose_name='وضعیت')
    due_date = models.DateField(verbose_name='تاریخ انجام')
    due_time = models.TimeField(blank=True,null=True,verbose_name='ساعت انجام')
    related_customer =models.ForeignKey('Costomer',on_delete=models.SET_NULL,blank=True,null=True,related_name='tasks',verbose_name='مشتری مرتبط')
    related_request =models.ForeignKey('CuostomerRequest',on_delete=models.SET_NULL,blank=True,null=True,related_name='tasks',verbose_name='درخواست مرتبط')
    related_property = models.ForeignKey('property.PropertyListing',on_delete=models.SET_NULL,blank=True,null=True,related_name='tasks',verbose_name='ملک مرتبط')
    is_auto_created =models.BooleanField(default=False,verbose_name='ایجاد خودکار')
    sms_reminder_enabled =models.BooleanField(default=False,verbose_name='پیامک یاداوری')
    sms_sent = models.BooleanField(default=False,verbose_name='پیامک ارسال شده')
    sms_sent_as= models.DateTimeField(null=True,blank=True,verbose_name='زمان ارسال پیامک')
    completed_at = models.DateTimeField(blank=True,null=True,verbose_name='زمان انجام')
    created_at=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد')
    updated_at=models.DateTimeField(auto_now=True,verbose_name='تاریخ بروزرسانی')

    class Meta :
        ordering=['status','due_date','due_time','-created_at']
        verbose_name = 'کار'
        verbose_name_plural='کار ها'

    def __str__(self):
        return f"{self.title}-{self.agent}"

    #کار های عقب افتاده
    @property
    def is_overdue(self):
        return self.status =='todo' and self.due_date <timezone.localdate()

    #کار های روزانه
    @property
    def is_today(self):
        return self.due_date==timezone.localdate()
