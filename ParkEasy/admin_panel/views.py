from django.shortcuts import render, redirect
from django.contrib import messages
from parkings.models import UserProfile


def is_superuser(user):
    return user.is_superuser


def superuser_required(function=None, redirect_field_name=None, login_url=None):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not is_superuser(request.user):
                messages.error(request, "You don't have sufficient rights to access this page")
                return redirect('/login/')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    if function:
        return decorator(function)
    return decorator


@superuser_required(login_url='/login/')
def home(request):
    return render(request, 'admin_panel/home.html')


@superuser_required(login_url='/login/')
def users(request):
    users = UserProfile.objects.all()
    return render(request, 'admin_panel/users.html', {'users': users})
