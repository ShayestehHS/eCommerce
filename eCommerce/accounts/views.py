from django.contrib import messages
from django.contrib.auth import login as login_user, logout as logout_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, FormView, ListView, UpdateView

from accounts.forms import ConfirmForm, RegisterForm, LoginForm, ChangeDetailForm
from carts.models import Cart
from eCommerce.utils import custom_send_email, required_ajax
from eCommerce.mixins import MessageMixin, NextUrlMixin, RequestFormAttachMixin

User = get_user_model()


class Register(CreateView, MessageMixin):
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    http_method_names = ['post', 'get']

    def get_success_url(self):
        base_url = reverse('accounts:confirm')
        return base_url + f"?uuc={self.object.unique_code}"


class ConfirmView(FormView):
    form_class = ConfirmForm
    http_method_names = ['post', 'get']
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/confirm.html'
    user_unique_code = None

    def get(self, request, *args, **kwargs):
        self.user_unique_code = self.request.GET.get('uuc')
        user = User.objects.get(unique_code=self.user_unique_code)
        if user.is_registered:
            messages.error(request, 'You are active.')
            return redirect('home')

        return super(ConfirmView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = User.objects.filter(unique_code=self.user_unique_code) \
            .only('chance_to_try', 'confirm_code', 'unique_code').first()

        if not user:
            messages.error(self.request, "You don't have permission to do this action.")
            return redirect('home')

        if not user.chance_to_try >= 1:  # Valid chance_to_try: 3,2,1
            # Out of chance
            messages.error(self.request, "You can't try anymore.")
            user.fail_activation()
            return redirect('home')

        confirm_code_val = form.cleaned_data['confirm_code']
        user.chance_to_try -= 1
        if user.confirm_code != confirm_code_val:
            if user.chance_to_try == 0:
                # Out of chance
                messages.error(self.request, "You can't try anymore.")
                user.fail_activation()
                return redirect('home')

            form.add_error('confirm_code', 'Confirm code is not true.')
            user.save(update_fields=['chance_to_try'])
            return super(ConfirmView, self).form_invalid(form)

        user.register()
        Cart.objects.new(self.request)

        login_user(request=self.request, user=user)
        return super(ConfirmView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ConfirmView, self).get_context_data(**kwargs)
        user_chance = User.objects.filter(unique_code=self.request.GET.get('uuc')) \
            .only('chance_to_try').first()
        context.update({'chance_to_try': user_chance.chance_to_try})
        return context


class Login(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    http_method_names = ['post', 'get']
    template_name = 'accounts/login.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(self.request, 'You successfully logged in.')
            return redirect('home')

        self.success_url = self.get_success_url()
        return super(Login, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        # User is logged in.
        messages.success(self.request, 'You successfully logged in.')
        return super(Login, self).form_valid(form)


class ProfileAccount(LoginRequiredMixin, ListView):
    http_method_names = ['get']
    model = User
    template_name = 'accounts/profile.html'

    def get_queryset(self):
        return self.request.user


class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ChangeDetailForm
    template_name = 'accounts/update_detail_form.html'

    def get_object(self, queryset=None):
        return self.request.user


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


def resend_confirm_email(request):
    user = request.user
    not_permission_to_resend = not user.is_anonymous or user.is_authenticated or user.is_active
    if not_permission_to_resend:
        messages.error(request, "You don't have permission to do this action.")
        return redirect('home')

    user_unique_code = request.GET.get('uuc')
    user = User.objects.get(unique_code__iexact=user_unique_code)
    user.send_activation_email()
    base_url = reverse('accounts:confirm')
    messages.success(request, 'Email is sent successfully.')
    return HttpResponseRedirect(base_url + f"?uuc={user.unique_code}")
