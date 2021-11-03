import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, ListView

from accounts.forms import ConfirmForm, RegisterForm, LoginForm, ContactEmailForm
from accounts.utils import CustomLoginRequiredMixin, create_email_code, set_cart_to_user
from analytics.signals import user_logged_in_signal
from carts.models import Cart
from eCommerce.utils import get_admin_emails, is_valid_url, custom_send_email, required_ajax
from eCommerce.mixins import MessageMixin

User = get_user_model()


class Register(CreateView, MessageMixin):  # ToDo: Should send email confirmation
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    http_method_names = ['post', 'get']
    uuc = None  # User Unique Code

    def form_valid(self, form):
        form.instance.unique_code = self.uuc = uuid.uuid4().hex[:16].upper()
        form.instance.confirm_code = confirm_code = create_email_code(6)
        custom_send_email(title="Email confirmation", to=[form.cleaned_data['email']],
                          context={'unique_code': confirm_code},
                          template_name='email/confirm_code.html')
        return super(Register, self).form_valid(form)

    def get_success_url(self):
        base_url = reverse('accounts:confirm')
        return base_url + f"?uuc={self.uuc}"


class ConfirmView(FormView):
    form_class = ConfirmForm
    http_method_names = ['post', 'get']
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/confirm.html'

    def form_valid(self, form):
        user_unique_code = self.request.GET.get('uuc')
        user = User.objects.filter(unique_code=user_unique_code) \
            .only('chance_to_try', 'confirm_code', 'unique_code').first()

        if not user:
            messages.error(self.request, "You don't have permission to do this action.")
            return redirect('home')

        if not user.chance_to_try >= 1:  # Valid chance_to_try: 3,2,1
            # Out of chance
            messages.error(self.request, "You can't try anymore.")
            user.delete()
            return redirect('home')

        confirm_code_val = form.cleaned_data['confirm_code']
        user.chance_to_try -= 1
        if user.confirm_code != confirm_code_val:
            if user.chance_to_try == 0:
                # Out of chance
                messages.error(self.request, "You can't try anymore.")
                user.delete()
                return redirect('home')

            form.add_error('confirm_code', 'Confirm code is not true.')
            user.save(update_fields=['chance_to_try'])
            return super(ConfirmView, self).form_invalid(form)

        user.is_registered = True
        user.save(update_fields=['chance_to_try', 'is_registered'])

        cart = Cart.objects.get(user=user)
        cart.is_active = True
        cart.save(update_fields=['is_active'])

        login_user(request=self.request, user=user)
        return super(ConfirmView, self).form_valid(form)

    def form_invalid(self, form):
        print('Form is invalid')
        return super(ConfirmView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(ConfirmView, self).get_context_data(**kwargs)
        user_chance = User.objects.filter(unique_code=self.request.GET.get('uuc')) \
            .only('chance_to_try').first()
        context.update({'chance_to_try': user_chance.chance_to_try})
        return context


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
            user = User.objects.filter(email=email).only('is_active').first()
            if not user.is_active:
                messages.error(request, 'This email is inactive')
            else:
                messages.error(request, 'Please try again.')
            return redirect('accounts:login')

        login_user(request, user)
        set_cart_to_user(request)
        user_logged_in_signal.send(user.__class__, instance=user, request=request)

        messages.success(request, 'You successfully logged in.')
        return redirect(self.get_success_url())


class ProfileAccount(CustomLoginRequiredMixin, ListView):
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
        custom_send_email(
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
