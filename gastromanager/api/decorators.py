from functools import wraps
from django.http import HttpResponseForbidden

def manager_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # for manager
        if request.user.is_authenticated and request.user.userprofile.is_manager:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No access")

    return _wrapped_view

def service_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # for service
        if request.user.is_authenticated and request.user.userprofile.is_service:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No access")

    return _wrapped_view

def production_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # for production
        if request.user.is_authenticated and request.user.userprofile.is_production:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("No access")

    return _wrapped_view