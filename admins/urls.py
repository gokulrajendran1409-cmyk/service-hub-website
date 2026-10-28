from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('admin_login/',views.admin_login,name="admin_login"),
    path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('admin_logout/',views.admin_logout,name="admin_logout"),
    path('professional_verification',views.professional_verification,name="professional_verification"),
    path('update_status/<int:id>/',views.update_status,name="update_status"),
    path('user_management/', views.user_management, name='user_management'),
    path('service_categories/',views.service_categories, name='service_categories'),
    path('booking_management/',views.booking_management,name='booking_management'),
]

