from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

from report.EmailReport import EmailReport
from .forms import IpForm, ScheduleForm, ScanForm, ContactForm
from .models import Ip, Scan, Schedule
from website.RedisManager import RedisManager
from django_ratelimit.decorators import ratelimit


def home(request):
    return render(request, "main/home.html", {"title": "Home", "breadcrumbs":{"Home": "/"}})

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
    
    return render(request, "main/add_ip.html", {'form': form,"title": "Add IP", "breadcrumbs": {"Home": "/", "Add IP": "/add_ip"}})

@login_required
def schedule(request):
    if request.method == "POST":
        form = ScheduleForm(request.user, request.POST)
        if form.is_valid():
            form.clean()
            try:
                ip = Ip.objects.get(ip_id=form.cleaned_data['ips'], user=request.user)
            except Ip.DoesNotExist:
                messages.add_message(request, messages.WARNING, "IP does not exist")
                return redirect("scan")
            schedule = Schedule(
                ip=ip,
                cron_time=form.get_cron_time(),
                scan_type=form.cleaned_data["scan_type"],  
                port_type=form.cleaned_data["port_type"]          
            )
            schedule.save()
            RedisManager.schedule(schedule.id)
            # Do something with the valid schedule object
            messages.add_message(request, messages.SUCCESS, "Schedule created successfully")
            return redirect("home")  # Redirect to a success page or another view
    else:
        return redirect("scan")
    
@login_required
def schedules(request, schedule_id):
    try:
        ip = Ip.objects.get(ip_id=schedule_id, user=request.user)
        schedules = Schedule.objects.filter(ip__user=request.user, ip=schedule_id)
    except Ip.DoesNotExist:
        return redirect("scan")
    except Schedule.DoesNotExist:
        return redirect("scan")    
    
    breadcrumbs = {
        "Home": "/",
        "Reports": f"/reports",
        "Schedules": f"/schedules/{schedule_id}",
    }
    
    return render(request, "main/schedules.html", {'title': 'Schedules', "ip":ip, 'schedules': schedules, "breadcrumbs": breadcrumbs})
    
@login_required
def delete_schedule(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id, ip__user=request.user)
    schedule.delete()
    RedisManager.delete_schedule(schedule_id)
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
                RedisManager.scan(ip=selected_ip.ip_id, scan_type=scan_type, port_type=ports)
                messages.success(request, "Scan started...")
                return redirect('home')
            messages.warning(request, f'You do not have permission to scan this IP')
    else:
        single_scan = ScanForm(user=request.user)
        schedule_scan = ScheduleForm(user=request.user)
    if single_scan.has_ips():
        breadcrumbs = {
            "Home": "/",
            "Scan": "/scan",
        }
        return render(request, 'main/scan.html', {'title': 'Scan', "scan_ip_now": single_scan, "schedule_ip_form": schedule_scan, "breadcrumbs": breadcrumbs})
    else:
        messages.warning(request, f'You do not have any IPs to scan')
        return redirect('home')


@login_required
def report(request):
    all_ips = Ip.objects.filter(user=request.user)
    breadcrumbs = {
        "Home": "/",
        "Reports": "/reports",
    }
    return render(request, 'report/report.html', {"breadcrumbs": breadcrumbs, 'ips': all_ips, 'title': 'Report'})

@login_required
def report_ip(request, ip_id):
    # Get all reports for ip
    ip = Ip.objects.get(ip_id=ip_id)
    if ip is None or ip.user != request.user: 
        return redirect('reports')
    scans = Scan.objects.filter(ip_id=ip_id)
    breadcrumbs = {
        "Home": "/",
        "Reports": "/reports",
        f"{ip.alias}": f"/reports/{ip.ip_id}",
    }
    return render(request, 'report/report_ip.html', {"breadcrumbs": breadcrumbs,"ip": ip,"scans": scans, 'title': 'Report'})

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
    
    breadcrumbs = {
        "Home": "/",
        "Reports": "/reports",
        f"{ip.alias}": f"/reports/{ip.ip_id}",
        f"scan": f"/reports/{ip.ip_id}/{scan.scan_id}",
    }
    
    return render(request, 'report/report_scan.html', {"breadcrumbs": breadcrumbs,'title': 'Report', "ip": ip, "scan": scan})


@ratelimit(key="user_or_ip", rate="3/m", method="POST")
def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            result = EmailReport.send_raw(subject=f"Contact Us - {form.cleaned_data['email']}", to_email=EmailReport.from_email, from_email=form.cleaned_data['email'], content=form.cleaned_data['message'])
            if(result):
                messages.success(request, "Message sent successfully")
            else:
                messages.error(request, "Message failed to send")
            return redirect('home')
    return render(request, 'main/contact.html', {'title': 'Contact', "form": form})
