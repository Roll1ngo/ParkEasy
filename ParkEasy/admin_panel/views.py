from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserProfileForm, PlateFormSet
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
    users = UserProfile.objects.prefetch_related('plates').all()
    return render(request, 'admin_panel/users.html', {'users': users})

#
# @superuser_required(login_url='/login/')
# def edit_user(request, user_id):
#     user = get_object_or_404(UserProfile, id=user_id)
#
#     if request.method == 'POST':
#         profile_form = UserProfileForm(request.POST, instance=user)
#         plates_formset = PlateFormSet(request.POST, instance=user)
#
#         if profile_form.is_valid() and plates_formset.is_valid():
#             profile_form.save()
#             plates_formset.save()
#             return redirect('admin_panel:users')
#     else:
#         profile_form = UserProfileForm(instance=user)
#         plates_formset = PlateFormSet(instance=user)
#
#     return render(request, 'admin_panel/edit_user.html', {
#         'profile_form': profile_form,
#         'plates_formset': plates_formset
#     })
#


@superuser_required(login_url='/login/')
def edit_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user)
        plates_formset = PlateFormSet(request.POST, instance=user)

        if profile_form.is_valid() and plates_formset.is_valid():
            profile_form.save()
            plates_formset.save()

            for form in plates_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    form.save()

            return redirect('admin_panel:users')  # Перенаправляємо після збереження
    else:
        profile_form = UserProfileForm(instance=user)
        plates_formset = PlateFormSet(instance=user)

    return render(request, 'admin_panel/edit_user.html', {
        'profile_form': profile_form,
        'plates_formset': plates_formset
    })
