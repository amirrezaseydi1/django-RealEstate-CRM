from django.shortcuts import render, redirect
from django.urls import reverse


class LeadsAccessMixin:
    allowed_roles = ['admin', 'manager', 'agent']
    no_permission_template = 'errors/no_permission.html'  # مسیر تمپلیت اختصاصی

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # ۱. اگر لاگین نیست -> هدایت به لاگین
        if not user.is_authenticated:
            return redirect(f"{reverse('accounts:login')}?next={request.path}")

        # ۲. سوپریوزر دسترسی کامل دارد
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # ۳. بررسی نقش
        profile = getattr(user, 'profile', None)
        if not profile or profile.role not in self.allowed_roles:
            # به جای raise کردن ارور، صفحه تمپلیت را مستقیماً نشان می‌دهیم
            return render(
                request,
                self.no_permission_template,
                {'error_message': 'شما به عنوان مشاور یا مدیر دسترسی لازم برای این بخش را ندارید.'},
                status=403
            )

        return super().dispatch(request, *args, **kwargs)
