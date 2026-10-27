from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.contrib import messages
from user.forms import userregform,bookingform
from user.models import userreg,Booking
from professional.models import proreg



def register(request):
    if request.method=="POST":
        form=userregform(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]

            if userreg.objects.filter(email__iexact=email).exists():
                return render(request, "register.html", {
                    "form": form,
                    "error": "This email is already registered!"
                })
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            messages.success(
                request,
                'Registration successful! Please log in to your account.'
            )
            return redirect('login')
        else:
            return render(request,'register.html',{'form':form})
           
    else:
        form=userregform()
    return render(request,'register.html',{'form':form})

def login(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")

        user = userreg.objects.filter(email=email).first()
        if user is not None:
            if check_password(password, user.password):
                request.session['email'] = user.email
                return redirect('userdashboard')
            return render(request,"login.html",{"error":"Invalid email or password"})
        
    return render(request,'login.html')

def userdashboard(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    customer = userreg.objects.filter(email__iexact=email).first()
    if customer is None:
        return redirect('login')
    bookings=Booking.objects.filter(customer=customer).order_by('-created_at')
    context ={

     'customer':customer, 
     'recent_bookings':bookings[:5],
     'total_bookings':bookings.count(),
     'pending_bookings':bookings.filter(status='pending').count(),
     'accepted_bookings':bookings.filter(status='accepted').count(),}

    return render(request,'userdashboard.html',context)

def logout(request):
    request.session.flush()
    return redirect('index')

def booking(request,id):
    email = request.session.get('email')

    if not email:
        login_url = reverse('login')
        next_url = reverse('booking', kwargs={'id': id})
        return redirect(f'{login_url}?next={next_url}')

    if not request.session.get('email'):
        return redirect('login')
    professional=get_object_or_404(proreg,id=id)

    if request.method=="POST":
        form=bookingform(request.POST)

        if form.is_valid():
            obj=form.save(commit=False)
            email = request.session.get('email')
            customer = get_object_or_404(userreg, email__iexact=email)
            obj.customer = customer
            obj.professional=professional
            obj.service_charge=professional.service_charge
            obj.save()

            messages.success(request,"booking successful")
            return redirect('userdashboard')

    else:
        form=bookingform()



    context={'professional':professional,
             'form':form,
             }
    return render(request,"booking.html",context)

def mybookings(request):
    email = request.session.get('email')

    if not email:
        return redirect('login')

    customer = get_object_or_404(userreg, email__iexact=email)

    bookings = Booking.objects.filter(
        customer=customer
    ).select_related('professional').order_by('-created_at')

    

    return render(request, 'my_booking.html', {
        'customer': customer,
        'bookings': bookings,
    })

def update_request(request, id):
    if request.method!='POST':
        return redirect('mybookings')
    email = request.session.get('email')
    if not email:
            return redirect('login')
    user=get_object_or_404(userreg,email=email)
    booking = get_object_or_404(
            Booking,
            id=id,
            customer=user
        )
    new_status = request.POST.get('status')
    if booking.status != 'pending':
            messages.warning(request, 'This booking has already been processed.')
    
    elif  new_status in ['accepted', 'rejected','cancelled']:
        booking.status = new_status
        booking.save(update_fields=['status'])
        messages.success(
                    request,
                    f'Booking #{booking.id} has been {new_status}.'
                )
    else:
        messages.error(request, 'status already accepted.')

    return redirect('mybookings')    