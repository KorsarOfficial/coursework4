from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView
import secrets
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from config.settings import EMAIL_HOST_USER
from django.core.exceptions import PermissionDenied
from users.forms import UsersRegisterForm, BlockingUser
from users.models import User


class UsersCreateView(CreateView):
    model = User
    form_class = UsersRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email_confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейдите по ссылке,"
                    f" чтобы завершить регистрацию и подтвердить почту {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class BlockingUsersView(LoginRequiredMixin,
                        PermissionRequiredMixin,
                        UpdateView):
    model = User
    form_class = BlockingUser
    template_name = "users/user_block_form.html"
    success_url = reverse_lazy("user:users_list")
    permission_required = "user.blocking_user"

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm("user.blocking_user"):
            raise PermissionDenied
        else:
            return BlockingUser


class UsersListView(LoginRequiredMixin,
                    PermissionRequiredMixin,
                    ListView):
    model = User
    template_name = "users/users_list.html"
    context_object_name = "users"
    permission_required = "user.view_user"

    def get_form_class(self):
        user = self.request.user
        if not user.has_perm("user.list_user"):
            raise PermissionDenied
