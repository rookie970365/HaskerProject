from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView, UpdateView, View

from questions.views import TrendingMixin

from .forms import LogInForm, ChangeForm, SignUpForm


class LogIn(TrendingMixin, FormView):
    form_class = LogInForm
    success_url = reverse_lazy("index")
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You have already logged in.")
            return redirect("index")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, "You have successfully logged in!")
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class LogOut(View):
    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.warning(self.request, "You are not authenticated!")
            return redirect("index")
        logout(self.request)
        messages.success(self.request, "You have successfully logged out.")
        return redirect("index")


class SignUp(TrendingMixin, CreateView):
    form_class = SignUpForm
    model = get_user_model()
    success_url = reverse_lazy("index")
    template_name = "signup.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.warning(self.request, "You have already logged in.")
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, *args, **kwargs):
        messages.success(self.request, "Thank you for registration!")
        return super().form_valid(*args, **kwargs)


class AccountDetail(TrendingMixin, LoginRequiredMixin, UpdateView):
    """ User settings view. Each user can edit only his/her own settings.
    """
    form_class = ChangeForm
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("detail")
    template_name = "detail.html"

    def form_valid(self, *args, **kwargs):
        messages.success(self.request, "Account details have been successfully updated!")
        return super().form_valid(*args, **kwargs)

    def form_invalid(self, *args, **kwargs):
        self.object.refresh_from_db()
        return super().form_invalid(*args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user
