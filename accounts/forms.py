from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserRegisterForm(forms.Form):
    user_name = forms.CharField(max_length=50,label='نام کاربری',widget=forms.TextInput(attrs={'placeholder':'نام کاربری','class':'form-control'}))
    email = forms.EmailField(label='پست الکتزونیکی',widget=forms.EmailInput(attrs={'placeholder':'Email...','class':'form-control'}))
    f_name = forms.CharField(max_length=50,label='نام',widget=forms.TextInput(attrs={'class':'form-control'}))
    l_name = forms.CharField(max_length=50,label='نام خانوادگی',widget=forms.TextInput(attrs={'class':'form-control'}))
    password_1=forms.CharField(max_length=50,label='رمز عبور',widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور','class':'form-control'}))
    password_2 = forms.CharField(max_length=50,label='تکرار رمزعبور',widget=forms.PasswordInput(attrs={'placeholder':'تکرار رمز عبور','class':'form-control'}))

    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        if User.objects.filter(username='user_name').exists():
            raise forms.ValidationError('نام کاربری تکزازس است ')
        return  user
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email='email').exists():
            raise forms.ValidationError('ایمیل وارد شده تکراری است ')
        return email
    def clean_password_2(self):
        pass1= self.cleaned_data['password_1']
        pass2 = self.cleaned_data['password_2']
        if pass1 != pass2 :
            raise forms.ValidationError('رمز وارد شده یکسان نیست')
        elif len(pass2) < 8 :
            raise forms.ValidationError('طول پسورد باید بیشتر از 8 کاراکتر باشد')
        elif not any(x.isupper() for x in pass2):
            raise forms.ValidationError('at least one upper case')
        return  pass2
class UserLoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری /ایمیل',widget=forms.TextInput(attrs={'placeholder':'ایمیل/نام کاربری','class':'form-control'}))
    password = forms.CharField(label='کلمه عبور',widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور','class':'form-control'}))



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class':'form-control'})