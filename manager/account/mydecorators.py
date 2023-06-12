from django.http import HttpResponseForbidden

def admin_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to access this page.")
    return wrapped_view

def customer_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_customer:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to access this page.")
    return wrapped_view

def employee_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_employee:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to access this page.")
    return wrapped_view

def supplier_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_supplier:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to access this page.")
    return wrapped_view
