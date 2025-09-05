from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# @login_required(login_url='/login/')   # redirect to login if not authenticated
def dashboard_home(request):
    if "access" not in request.session:
        return redirect("login_page")   # 👈 your custom login view name

    return render(request, "dashboard/home.html", {
        "access": request.session.get("access"),
        "refresh": request.session.get("refresh"),
    })
