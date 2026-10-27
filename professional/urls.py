from django.urls import path
from . import views

urlpatterns = [
    path('proregister',views.proregister,name="proregister"),
    path('prologin',views.prologin,name="prologin"),
    path('prodashboard',views.prodashboard,name="prodashboard"),
    path('my_bookings',views.my_bookings,name="my_bookings"),
    path('update-booking/<int:id>',views.update_booking_status,
    name='update_booking_status'
),
    path('prologout', views.prologout, name="prologout"),
    path('review/<int:id>/',views.add_review,name='add_review'
),
]