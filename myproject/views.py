from django.shortcuts import render
from professional.models import proreg

def index(request):
    return render(request,'index.html') 

def services(request):
    professionals=proreg.objects.filter(status='Approved')
    context={'professionals':professionals,
             }
    return render(request,'services.html',context)