from django.shortcuts import render
from .models import Ip


def home(request):
    return render(request, 'main/home-page.html', {'title': 'Home'})


def scan(request):
    all_ips = Ip.objects.all
    return render(request, 'main/scan.html', {'all': all_ips, 'title': 'Scan'})


def contact(request):
    return render(request, 'main/contact.html', {'title': 'Contact'})


def report(request):
    all_ips = Ip.objects.all
    return render(request, 'main/report.html', {'all': all_ips, 'title': 'Report'})


def login(request):
    return render(request, 'main/login.html', {'title': 'Login'})


def signup(request):
    return render(request, 'main/signup.html', {'title': 'Signup'})


def recover2(request):
    return render(request, 'main/forgotton-password.html', {'title': 'Recover2'})


def recover3(request):
    return render(request, 'main/forgotton-password-number.html', {'title': 'Recover3'})


def recover(request):
    return render(request, 'main/create-new-password.html', {'title': 'Recover'})
