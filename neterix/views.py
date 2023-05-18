from django.shortcuts import render
from .models import Ip


def home(request):
    all_ips=Ip.objects.all
    return render(request, 'index.html', {'all':all_ips})

def contact(request):
    return render(request, 'contact.html')

def report(request):
    all_ips=Ip.objects.all
    return render(request, 'report.html', {'all':all_ips})
