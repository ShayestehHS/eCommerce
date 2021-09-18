from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user, logout as logout_user
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model

from accounts.forms import LoginForm

User = get_user_model()


@require_http_methods(['GET', 'POST'])
def login(request):
    next_page = request.GET.get('next') or request.POST.get('next')
    form = LoginForm(request.POST or None)
    context = {'form': form}

    if form.is_valid():
        email = form.cleaned_data.get('email')
        if email not in User.objects.all().values_list('email', flat=True):
            messages.error(request, 'Your email is wrong')
            return redirect('accounts:login')
        password = form.cleaned_data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is None:
            messages.error(request, 'Please try again.')
            return redirect('accounts:login')
        login_user(request, user)
        messages.success(request, 'You successfully logged in.')

        if not is_safe_url(next_page, request.get_host()):
            return redirect('home')
        return redirect(next_page)
    return render(request, 'accounts/login.html', context)


def logout(request):
    logout_user(request)
    return redirect('home')
