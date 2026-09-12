from django.core.exceptions import PermissionDenied

class LeadsAccessMixin:
    allowed_roles=['admin','manager','agent']
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            raise PermissionDenied
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        profile = getattr(user, 'profile', None)
        if not profile or profile.role not in self.allowed_roles:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)