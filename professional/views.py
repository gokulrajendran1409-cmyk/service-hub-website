from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from professional.forms import proregform
from professional.models import proreg
from user.models import Booking


# Create your views here.
from django.http import HttpResponse

def proregister(request):
    if request.method=="POST":
        form=proregform(request.POST,request.FILES)
        if form.is_valid():
            email=form.cleaned_data["email"]

            if proreg.objects.filter(email__iexact=email).exists():
                return render(request,"proregister.html",{
                    "form":form,
                    "error":"this email is already registered!"})

            if form.cleaned_data["password"] != request.POST.get("confirm_password"):
                return render(request, "proregister.html", {
                    "form": form,
                    "error": "Passwords do not match!"
                })
           
            pro=form.save(commit=False)
            pro.password=make_password(pro.password)
            pro.save()
            messages.success(
                request,
                'registration sucesful! please log in to your acount.'

            )
            return redirect('prologin')

    else:
        form=proregform()
    return render(request,"proregister.html",{'form':form})

def prologin(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password =request.POST.get("password")

        pro=proreg.objects.filter(email__iexact=email).first()
        
        if pro is  None:
            return render (request,"prologin.html",{"error":"Invalid email or password"})

        if not check_password(password,pro.password):
            
            return render(request,"prologin.html",{"error":"Invalid email or password"})
        
        if pro.status.lower() == "approved":
            request.session['email']=pro.email
            return redirect("prodashboard")

        elif pro.status.lower() == "rejected":
            return render (request,"prologin.html",{"error":"Your request is rejected "})
        else:
            return render (request,"prologin.html",{"error":"your request is still pending"})

    return render(request,"prologin.html")

def prodashboard(request):
    if not request.session.get('email'):
        messages.error(request,"please log in as a professional")
        return redirect('prologin')

    professional=proreg.objects.filter(email=request.session['email']).first()

    if professional is None:
        messages.error(request,"professional account not fount")
        return redirect('prologin')

    bookings=Booking.objects.filter(professional=professional).order_by('created_at')

    context={
        'professional':professional,
        'recent_bookings':bookings[:5],
        'total_bookings':bookings.count(),
        'pending_bookings':bookings.filter(status='pending').count(),
        'completed_bookings':bookings.filter(status='completed').count(),

    }
    return render(request,"prodashboard.html",context)

def my_bookings(request):
    # Check professional login
    email = request.session.get('email')

    if not email:
        return redirect('prologin')

    # Get the logged-in professional
    professional = get_object_or_404(proreg, email=email)

    # Show only bookings assigned to this professional
    bookings = Booking.objects.filter(
        professional=professional
    ).select_related('customer').order_by('-created_at')

    context = {
        'professional': professional,
        'bookings': bookings,
    }

    return render(request, 'my_bookings.html', context)


def update_booking_status(request, id):
    if request.method != 'POST':
        return redirect('my_bookings')

    email = request.session.get('email') or request.session.get('professional_email')

    if not email:
        return redirect('prologin')

    professional = get_object_or_404(proreg, email=email)

    # Ensure this booking belongs to the logged-in professional
    booking = get_object_or_404(
        Booking,
        id=id,
        professional=professional
    )

    new_status = request.POST.get('status')

    if booking.status != 'pending':
        messages.warning(request, 'This booking has already been processed.')

    elif new_status in ['accepted', 'rejected']:
        booking.status = new_status
        booking.save(update_fields=['status'])

        messages.success(
            request,
            f'Booking #{booking.id} has been {new_status}.'
        )

    else:
        messages.error(request, 'Invalid booking status.')

    return redirect('my_bookings')


def prologout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('prologin')