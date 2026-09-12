from django.shortcuts import render  ,redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login ,logout
from django.contrib import messages
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import  update_session_auth_hash
from django.contrib.auth.decorators import login_required
# Create your views here.
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid() :
            data = form.cleaned_data
            user = User.objects.create_user(
                username= data['user_name'],
                email = data['email'],
                first_name = data['f_name'],
                last_name = data['l_name'],
                password=data['password_2']
            )
            user.save()
            messages.success(request , 'ثبت نام شما با موفقیت انجام شد' , 'success')
            return redirect('home:home')
    else:
        form = UserRegisterForm()
    return render(request,'accounts/register.html',context={'form':form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            identifier = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # ابتدا تلاش برای ورود با نام کاربری
            user = authenticate(
                request,
                username=identifier,
                password=password
            )

            # اگر لاگین با username ناموفق بود، ایمیل را بررسی می‌کنیم
            if user is None:
                try:
                    user_obj = User.objects.get(email=identifier)

                    user = authenticate(
                        request,
                        username=user_obj.username,
                        password=password
                    )

                except User.DoesNotExist:
                    pass

            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید.')

                next_url = request.POST.get('next')
                return redirect(next_url or 'home:home')

            messages.error(
                request,
                'نام کاربری/ایمیل یا رمز عبور نادرست است.'
            )

    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})
def user_logout(request):
    logout(request)
    messages.success(request,'با موفقّیت خارج شدید ','warning')
    return  redirect('home:home')

@login_required(login_url='accounts:login')
def user_profile(request):
        profile = Profile.objects.get(user_id=request.user.id)
        return render(request,'accounts/profile.html',context={'profile':profile})
@login_required(login_url='accounts:login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,instance=request.user.profile)
        if user_form.is_valid() and profile_form .is_valid():
            user_form.save()
            profile_form.save()
        return redirect('accounts:profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'accounts/update.html', {'user_form': user_form, 'profile_form':profile_form})

@login_required(login_url='accounts:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user= form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
        return  render (request,'accounts/changepassword.html',context={'form':form})
