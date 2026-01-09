from rest_framework import permissions

class IsPremiumPro(permissions.BasePermission):
    """
    Sadece Premium Pro aboneliği olan kullanıcıların erişimine izin verir.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            (request.user.subscription_level == 'premium_pro' or request.user.is_staff)
        )
