from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import View


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


def home(request):
    return render(request, "home.html")


class RegisterView(View):
    template_name = "register.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        form = CustomUserCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Cuenta creada exitosamente. Inicia sesión.")
            return redirect("login")
        return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido {user.username}")
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("dashboard")
        messages.error(request, "Usuario o contraseña incorrectos")
        return render(request, self.template_name)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Sesión cerrada correctamente")
        return redirect("login")


class DashboardView(LoginRequiredMixin, View):
    template_name = "dashboard.html"

    def get(self, request):
        user_permissions = request.user.get_all_permissions()
        return render(request, self.template_name, {
            "user": request.user,
            "permissions": sorted(user_permissions),
        })


class ProfileView(LoginRequiredMixin, View):
    template_name = "profile.html"

    def get(self, request):
        return render(request, self.template_name, {"user": request.user})


@login_required
@permission_required("auth.view_user", raise_exception=True)
def admin_users(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, "admin_users.html", {"users": users})


class ModerateContent(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "auth.change_user"
    template_name = "moderate.html"

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            return render(self.request, "403.html", status=403)
        return super().handle_no_permission()

    def get(self, request):
        return render(request, self.template_name)
