from django.shortcuts import render
from .models import Ip


def home(request):
    return render(request, 'main/home.html', {'title': 'Home'})


def scan(request):
    all_ips = Ip.objects.all
    return render(request, 'main/scan.html', {'all': all_ips, 'title': 'Scan'})


def contact(request):
    return render(request, 'main/contact.html', {'title': 'Contact'})


def report(request):
    all_ips = Ip.objects.all
    return render(request, 'main/report.html', {'all': all_ips, 'title': 'Report'})
