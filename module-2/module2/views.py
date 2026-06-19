from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from portal.forms import AdminLoginForm, LoginForm, MobileApplicationForm, RegistrationForm, ReviewForm
from portal.models import Application, Review


def login_view(request):
    if request.user.is_authenticated:
        return redirect("module2:cabinet")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.cleaned_data["user"])
        messages.success(request, "Вход выполнен.")
        return redirect("module2:cabinet")
    return render(request, "module2/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("module2:cabinet")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Аккаунт создан.")
        return redirect("module2:cabinet")
    return render(request, "module2/register.html", {"form": form})


@login_required(login_url="module2:login")
def cabinet_view(request):
    applications = (
        Application.objects.filter(user=request.user)
        .select_related("review")
        .order_by("-created_at", "-id")
    )
    if request.method == "POST":
        application = get_object_or_404(Application, pk=request.POST.get("application_id"), user=request.user)
        if application.status == Application.STATUS_NEW:
            messages.error(request, "Отзыв доступен после изменения статуса администратором.")
            return redirect("module2:cabinet")
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.update_or_create(
                application=application,
                defaults={"user": request.user, "text": form.cleaned_data["text"]},
            )
            messages.success(request, "Отзыв сохранен.")
            return redirect("module2:cabinet")
    return render(request, "module2/cabinet.html", {"applications": applications, "review_form": ReviewForm()})


@login_required(login_url="module2:login")
def request_view(request):
    form = MobileApplicationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.user = request.user
        application.status = Application.STATUS_NEW
        application.save()
        messages.success(request, "Заявка отправлена на согласование.")
        return redirect("module2:cabinet")
    return render(request, "module2/request.html", {"form": form})


def admin_view(request):
    if request.method == "POST" and request.POST.get("action") == "login":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            request.session["module2_admin"] = True
            messages.success(request, "Панель администратора открыта.")
            return redirect("module2:admin")
    elif request.method == "POST" and request.session.get("module2_admin"):
        application = get_object_or_404(Application, pk=request.POST.get("application_id"))
        application.status = request.POST.get("status", application.status)
        application.save()
        messages.success(request, "Статус заявки обновлен.")
        return redirect(f"{request.path}?{request.GET.urlencode()}")
    else:
        form = AdminLoginForm()

    applications = Application.objects.none()
    page_obj = None
    if request.session.get("module2_admin"):
        applications = Application.objects.select_related("user", "user__profile").order_by("-created_at", "-id")
        search = request.GET.get("search", "").strip()
        status = request.GET.get("status", "").strip()
        transport = request.GET.get("transport", "").strip()
        sort = request.GET.get("sort", "created_desc")

        if search:
            applications = applications.filter(
                Q(user__profile__full_name__icontains=search)
                | Q(user__username__icontains=search)
                | Q(user__profile__phone__icontains=search)
            )
        if status:
            applications = applications.filter(status=status)
        if transport:
            applications = applications.filter(transport=transport)

        if sort == "date_asc":
            applications = applications.order_by("start_date", "id")
        elif sort == "name_asc":
            applications = applications.order_by("user__profile__full_name", "id")

        page_obj = Paginator(applications, 3).get_page(request.GET.get("page"))

    context = {
        "form": form,
        "applications": applications,
        "page_obj": page_obj,
        "status_choices": Application.STATUS_CHOICES,
        "transport_choices": Application.TRANSPORT_CHOICES,
        "query": request.GET,
    }
    return render(request, "module2/admin.html", context)


def logout_view(request):
    logout(request)
    return redirect("module2:login")
