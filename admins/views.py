from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from professional.models import proreg
from user.models import userreg,category,Booking
from django.db.models import Q

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


def user_management(request):
    # Apply the same admin-session validation used by admin_dashboard.
    users = userreg.objects.all().order_by('-id')

    context = {
        'users': users,
        'total_users': users.count(),
    }
    return render(request, 'user_management.html', context)

def service_categories(request):
    categories = category.objects.all().order_by('id')

    return render(request, 'service_categories.html', {
        'categories': categories,
        'total_categories': categories.count(),
    })


def booking_management(request):
    bookings = Booking.objects.select_related(
        'customer', 'professional'
    ).order_by('-created_at')

    search = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()

    if search:
        bookings = bookings.filter(
            Q(customer__name__icontains=search) |
            Q(customer__email__icontains=search) |
            Q(professional__name__icontains=search) |
            Q(service_description__icontains=search) |
            Q(service_address__icontains=search) |
            Q(contact_number__icontains=search)
        )

    valid_statuses = [choice[0] for choice in Booking.STATUS_CHOICES]
    if status_filter in valid_statuses:
        bookings = bookings.filter(status=status_filter)

    context = {
        'bookings': bookings,
        'total_bookings': Booking.objects.count(),
        'pending_bookings': Booking.objects.filter(status='pending').count(),
        'completed_bookings': Booking.objects.filter(status='completed').count(),
        'search': search,
        'status_filter': status_filter,
        'status_choices': Booking.STATUS_CHOICES,
    }

    return render(request, 'booking_management.html', context)