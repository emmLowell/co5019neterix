from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import ScanForm
from .models import Ip, Scan


def home(request):
    return render(request, 'main/home.html', {'title': 'Home'})


@login_required
def scan(request):
    if request.method == 'POST':
        form = ScanForm(request.user, request.POST)
        if form.is_valid():
            scan_type = form.cleaned_data['scan_type']
            ports = form.cleaned_data['ports']
            selected_ip_id = form.cleaned_data['ips']
            
            # Perform operations based on the selected options and IP
            selected_ip = Ip.objects.get(ip_id=selected_ip_id)
            if(selected_ip.user == request.user):
                messages.success(request, "Scan started...")
                # TODO - report back on scan
                return redirect('home')
            messages.warning(request, f'You do not have permission to scan this IP')
    else:
        form = ScanForm(user=request.user)
    if form.has_ips():
        return render(request, 'main/scan.html', {'title': 'Scan', "form": form})
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