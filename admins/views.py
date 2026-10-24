from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from professional.models import proreg

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "admin123" and password =="admin123":
            return redirect('admin_dashboard')
        else:
            messages.error(request,"invalid username or password")
    return render(request,"admin_login.html")

def admin_dashboard(request):
    total_professionals = proreg.objects.count()
    pending_professionals = proreg.objects.filter(status__iexact="pending").count()
    approved_professionals = proreg.objects.filter(status__iexact="approved").count()
    rejected_professionals = proreg.objects.filter(status__iexact="rejected").count()

    recent_professionals = proreg.objects.order_by("-id")[:5]

    context= {
        "total_professionals":total_professionals,
        'pending_professionals':pending_professionals,
        'approved_professionals':approved_professionals,
        'rejected_professionals':rejected_professionals,
        'recent_professionals':recent_professionals,}

    return render(request,"admin_dashboard.html",context)

def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')

def professional_verification(request):
    total_professionals = proreg.objects.count()
    pending_professionals = proreg.objects.filter(status__iexact="pending").count()
    approved_professionals = proreg.objects.filter(status__iexact="approved").count()
    rejected_professionals = proreg.objects.filter(status__iexact="rejected").count()
    professionals = proreg.objects.all().order_by("-id")

    context= {
            "total_professionals":total_professionals,
            'pending_professionals':pending_professionals,
            'approved_professionals':approved_professionals,
            'rejected_professionals':rejected_professionals,
            'professionals':professionals,
            }
    
    return render(request,"professional_verification.html",context)

def update_status(request,id):
    reg=get_object_or_404(proreg,id=id)
    status =request.POST.get('status')

    if status == 'approved':
        reg.status='Approved'

    elif status == 'rejected' :
        reg.status='Rejected'

    else :
        return redirect('professional_verification')    

    reg.save(update_fields=['status'])
    return redirect('professional_verification')
