from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user, logout as logout_user
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model

from accounts.forms import LoginForm
from accounts.utils import set_cart_to_user
from eCommerce.utils import is_valid_url


User = get_user_model()


@require_http_methods(['GET', 'POST'])
def login(request):
    form = LoginForm(request.POST or None)

    if not form.is_valid():
        context = {'form': form}
        return render(request, 'accounts/login.html', context)

    # get values from Form
    email = form.cleaned_data.get('email')
    if email not in User.objects.all().values_list('email', flat=True):
        messages.error(request, 'Your email is wrong')
        return redirect('accounts:login')
    password = form.cleaned_data.get('password')

    # Login the user
    user = authenticate(request, email=email, password=password)
    if user is None:
        messages.error(request, 'Please try again.')
        return redirect('accounts:login')
    login_user(request, user)
    messages.success(request, 'You successfully logged in.')

    set_cart_to_user(request)

    # redirect user
    next_page = request.GET.get('next') or request.POST.get('next')
    if not is_valid_url(request, next_page):
        return redirect('home')
    return redirect(next_page)


def logout(request):
    logout_user(request)
    messages.success(request, 'You successfully logged out.')
    return redirect('home')
