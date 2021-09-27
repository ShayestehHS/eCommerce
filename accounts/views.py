from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user, logout as logout_user
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.views.generic import CreateView

from accounts.forms import LoginForm, ContactEmailForm
from accounts.utils import set_cart_to_user
from eCommerce.utils import get_admin_emails, is_valid_url, EmailService

User = get_user_model()


class ContactEmailCreate(CreateView):  # ToDo: Handle by AJAX
    form_class = ContactEmailForm
    template_name = 'accounts/contact.html'
    context_object_name = 'form'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user if self.request.user.is_authenticated else None
        form.save()
        EmailService.send_email(
            title=f'Contact email from {form.email}',
            to=get_admin_emails(),
            context={'msg_model': form},
            template_name='email/contact_email.html'
        )
        # self.message = 'Your message is received'
        return JsonResponse({})


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
