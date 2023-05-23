from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ScheduleForm
from .models import Ip


def home(request):
    return render(request, "main/home.html", {"title": "Home"})


def schedule(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save()
            # Do something with the valid schedule object
            messages.add_message(request, messages.SUCCESS, "Schedule created successfully")
            return redirect("home")  # Redirect to a success page or another view
    else:
        form = ScheduleForm()

    return render(request, "create_schedule.html", {"form": form})


def scan(request):
    all_ips = Ip.objects.all
    return render(request, "main/scan.html", {"all": all_ips, "title": "Scan"})


def contact(request):
    return render(request, "main/contact.html", {"title": "Contact"})


def report(request):
    all_ips = Ip.objects.all
    return render(request, "main/report.html", {"all": all_ips, "title": "Report"})
