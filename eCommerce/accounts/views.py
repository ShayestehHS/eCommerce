from django.contrib import messages
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, ListView

from accounts.forms import RegisterForm, LoginForm, ContactEmailForm
from accounts.utils import set_cart_to_user
from analytics.signals import user_logged_in_signal
from eCommerce.utils import get_admin_emails, is_valid_url, EmailService, required_ajax
from eCommerce.mixins import MessageMixin

User = get_user_model()


class Register(CreateView, MessageMixin):  # ToDo: Should send email confirmation
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    http_method_names = ['post', 'get']

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url and is_valid_url(self.request, next_url):
            return next_url
        return self.success_url


class Login(FormView, MessageMixin):
    http_method_names = ['post', 'get']
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url and is_valid_url(self.request, next_url):
            return next_url
        return self.success_url

    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is None:
            messages.error(request, 'Please try again.')
            return redirect('accounts:login')

        login_user(request, user)
        set_cart_to_user(request)
        user_logged_in_signal.send(user.__class__, instance=user, request=request)

        messages.success(request, 'You successfully logged in.')
        return redirect(self.get_success_url())


class ProfileAccount(LoginRequiredMixin, ListView):
    http_method_names = ['get']
    model = User
    template_name = 'accounts/profile.html'

    def get_queryset(self):
        return self.request.user


class ContactEmailCreate(CreateView, MessageMixin):
    http_method_names = ['post']
    message = 'Your message is received'
    message_level = messages.SUCCESS
    form_class = ContactEmailForm
    template_name = 'accounts/contact.html'
    context_object_name = 'form'

    @method_decorator(required_ajax)
    def dispatch(self, request, *args, **kwargs):
        return super(ContactEmailCreate, self).dispatch(request, *args, **kwargs)

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
        return JsonResponse({})

    def form_invalid(self, form):
        self.message = 'You form is not valid'
        self.message_level = messages.ERROR
        return super(ContactEmailCreate, self).form_invalid(form)

    def get_initial(self):
        user = self.request.user if self.request.user.is_authenticated else None
        if user is None:
            return super(ContactEmailCreate, self).get_initial()

        return {'email': user.email, 'full_name': user.full_name}


def logout(request):
    logout_user(request)
    messages.success(request, 'You successfully logged out.')
    return redirect('home')


@required_ajax
def check_email(request):
    email = request.GET.get('email')
    if email is None or request.method != 'GET':
        return JsonResponse({})

    email_exists = User.objects.filter(email=email).exists()
    return JsonResponse({'email_exists': not email_exists})
