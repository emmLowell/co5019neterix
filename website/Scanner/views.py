from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import IpForm, ScheduleForm
from .forms import ScanForm
from .models import Ip, Scan, Schedule


def home(request):
    return render(request, "main/home.html", {"title": "Home"})

@login_required
def add_ip(request):
    if request.method == 'POST':
        form = IpForm(request.POST)
        if form.is_valid():
            ip = form.save(commit=False)
            ip.user = request.user
            ip.save()
            messages.success(request, "IP added successfully")
            return redirect('home') 
    else:
        form = IpForm()
    
    return render(request, "main/add_ip.html", {'form': form,"title": "Add IP"})

@login_required
def schedule(request):
    if request.method == "POST":
        form = ScheduleForm(request.user, request.POST)
        if form.is_valid():
            # Do something with the valid schedule object
            messages.add_message(request, messages.SUCCESS, "Schedule created successfully")
            return redirect("home")  # Redirect to a success page or another view
    else:
        return redirect("scan")
    
@login_required
def schedules(request, schedule_id):
    schedules = Schedule.objects.filter(ip__user=request.user, ip=schedule_id)
    
    return render(request, "main/schedules.html", {'title': 'Schedules', 'schedules': schedules})
    
@login_required
def delete_schedule(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id, ip__user=request.user)
    schedule.delete()
    messages.add_message(request, messages.SUCCESS, "Schedule deleted successfully")
    return redirect("home")
    
@login_required
def scan(request):
    if request.method == 'POST':
        single_scan = ScanForm(request.user, request.POST)
        if single_scan.is_valid():
            scan_type = single_scan.cleaned_data['scan_type']
            ports = single_scan.cleaned_data['ports']
            selected_ip_id = single_scan.cleaned_data['ips']
            
            # Perform operations based on the selected options and IP
            selected_ip = Ip.objects.get(ip_id=selected_ip_id)
            if(selected_ip.user == request.user):
                messages.success(request, "Scan started...")
                # TODO - report back on scan
                return redirect('home')
            messages.warning(request, f'You do not have permission to scan this IP')
    else:
        single_scan = ScanForm(user=request.user)
        schedule_scan = ScheduleForm(user=request.user)
    if single_scan.has_ips():
        return render(request, 'main/scan.html', {'title': 'Scan', "scan_ip_now": single_scan, "schedule_ip_form": schedule_scan})
    else:
        messages.warning(request, f'You do not have any IPs to scan')
        return redirect('home')


@login_required
def report(request):
    all_ips = Ip.objects.filter(user=request.user)
    return render(request, 'report/report.html', {'ips': all_ips, 'title': 'Report'})

@login_required
def report_ip(request, ip_id):
    # Get all reports for ip
    ip = Ip.objects.get(ip_id=ip_id)
    if ip is None or ip.user != request.user: 
        return redirect('reports')
    scans = Scan.objects.filter(ip_id=ip_id)
    return render(request, 'report/report_ip.html', {"ip": ip,"scans": scans, 'title': 'Report'})

@login_required
def report_scan(request, ip_id, scan_id):
    messages.success(request, "Report for scan")
    ip = Ip.objects.get(ip_id=ip_id)
    scan = Scan.objects.get(ip_id=ip_id, scan_id=scan_id)
    if ip is None or ip.user != request.user:
        messages.warning(request, f'You do not have permission to view this IP')
        return redirect('reports')
    if scan is None:
        messages.warning(request, f'You do not have permission to view this scan')
        return redirect('report_ip', ip_id=ip_id)
    
    return render(request, 'report/report_scan.html', {'title': 'Report', "ip": ip, "scan": scan})

def contact(request):
    return render(request, 'main/contact.html', {'title': 'Contact'})
