from django.urls import path 
from . import views 

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.user_login,name='login'),
    path('register/',views.register,name='register'),
    path('register_property/',views.register_property,name='register_property'),
    path('payment/<int:id>/',views.payment,name='payment'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('success/', views.payment_success, name='payment_success'),
    path('adminDashboard/',views.adminDashboard,name='adminDashboard'),
    path('accept/<int:id>',views.accept,name='accept'),
    path('reject/<int:id>',views.reject,name='reject'),
    path('generate_certificate/<int:id>',views.generate_certificate,name='generate_certificate'),
    path('logout/',views.user_logout,name='logout'),
    
   
]