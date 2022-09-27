

from django.urls import path, register_converter

from main.converters import DateConverter 
from . import views 

register_converter(DateConverter, 'date')

urlpatterns = [
    path('', views.nopath , name='nopath') ,
    path('home', views.home , name='home') ,
    path('login', views.login_view , name='login') ,
    path('logout', views.logout_view , name='logout') ,
    path('register', views.register_view , name='register') ,
    path('contact_us',views.contact_us_view , name='contact_us'),
    path('doctors',views.doctors , name='doctors'),
    path('patient_file',views.patient_file , name='patient_file'),
    path('patient_file/<int:id>',views.d_to_patient_file , name='patient_file'),
    path('doctor_book/<int:id>',views.doctor_book , name='doctor_book'),
    path('get_modelAPI/<int:id>',views.get_modelAPI , name='get_modelAPI'),
    path('get_appointment/<int:id>/<date:apdate>',views.get_appointment , name='get_appointment'),
    path('book_appointment/<int:doctor_id>/',views.book_appointment , name='book_appointment'),
    path('patient_file/appointments', views.patient_appointments, name='patient_appointments'),
    path('doctor_dashboard', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor_dashboard/doctor_appointment', views.doctor_appointment, name='doctor_appointment'),
    path('doctor_dashboard/work_time', views.work_time, name='work_time'),
    path('doctor_dashboard/doctor_appointment/attendace/<int:appointment_id>/', views.attendace, name='attendace'),

    

    


]
