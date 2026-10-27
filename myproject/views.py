from django.shortcuts import render,get_object_or_404
from django.db.models import Avg, Count
from professional.models import proreg,Review
from user.models import category


def index(request):
    return render(request,'index.html') 

def services(request, id):
    selected_service = get_object_or_404(category, id=id)

    professionals = proreg.objects.filter(
        category__iexact=selected_service.name,
        status='Approved'
    ).annotate(
        average_rating=Avg('reviews__rating'),
        total_reviews=Count('reviews')
    )

    context = {
        'professionals': professionals,
        'selected_service': selected_service,
    }

    return render(request, 'services.html', context)


def all_services(request):

    service=category.objects.all()
    total_categories = category.objects.count()
    context={'service':service,
             'total_categories':total_categories,}
    return render(request,"all_services.html",context)