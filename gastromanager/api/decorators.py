from functools import wraps
from django.http import HttpResponseForbidden

def manager_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user's level is "Manager"
        if request.user.is_authenticated and request.user.userprofile.level == 'Manager':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No access")

    return _wrapped_view

def service_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user's level is "Service"
        if request.user.is_authenticated and request.user.userprofile.level == 'Service':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No access")

    return _wrapped_view

def production_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user's level is "Production"
        if request.user.is_authenticated and request.user.userprofile.level == 'Production':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No access")

    return _wrapped_view