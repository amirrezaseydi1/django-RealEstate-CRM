from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save ,post_delete
# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES=[
        ('agent','مشاور'),
        ('manager','مدیر'),
        ('admin','ادمین'),
        ('user','کاربر عادی')
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='user',verbose_name='نقش')
    # is_agent = models.BooleanField( blank=True,null=True,default=False,verbose_name='مشاور')
    phone = models.CharField(max_length=11,null=True,blank=True)
    address  = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.user.username
    @property
    def is_agent(self):
        return self.role =="agent"
    @property
    def is_manager(self):
        return self.role == 'manger'
    def is_admin_role(self):
        return self.role =='admin'

def save_profile_user(sender,**kwargs):
    if kwargs['created']:
        profile_user = Profile(user = kwargs['instance'])
        profile_user.save()

post_save.connect(save_profile_user,sender=User)





