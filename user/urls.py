from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('userdashboard/',views.userdashboard,name='userdashboard'),
    path('logout/', views.logout, name='logout'),
    path('booking/<int:id>/',views.booking,name="booking"),
    path('mybookings/', views.mybookings, name='mybookings'),
    path('update_request/<int:id>/',views.update_request,name="update_request"),
]