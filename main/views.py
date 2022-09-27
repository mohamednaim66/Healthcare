from ast import Or
from asyncio.windows_events import NULL
from cgi import print_arguments
from cgitb import text
from datetime import date, time, timedelta,datetime
from distutils.command.sdist import sdist
from distutils.log import error
import json
from time import strftime, strptime
from urllib.request import Request
from xmlrpc.client import DateTime
from django.conf import Settings, settings
from django.forms import CharField
from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import redirect, render
from numpy import require
from main.forms import AppointmentForm, ContactUsForm, PatientRegisterForm, RegisterUserForm, RegisterUserInfoForm, Worktime
from main.models import Appointment, Area, City, Day, Offer, PatientRegister, Specialty,UserInfo
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language,activate,gettext
from django.core.paginator import Paginator
from django.core import serializers
from django.db.models.functions import Concat
from django.db.models import Value

from django.db.models import Q

from main.templatetags.extra_filter import dayVal


# Create your views here.

def nopath(request):
    return redirect('home')

def home(request):
    Offers = Offer.objects.all()[0:8]
    Specialties = Specialty.objects.all()
    Cities = City.objects.all()
    return render(request,'home.html',{'Specialties':Specialties,'Offers':Offers ,'Cities':Cities } )

def login_view(request):
    next = NULL
    if request.user.is_authenticated:
        return redirect(home)
    if request.GET.get('next'):
        next=request.GET['next']


    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not request.POST.get('rememberMe') :
                request.session.set_expiry(0)

            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET['next'])
            else:
                return redirect('home')


        else:
            messages.error(request,_('username or password is wrong'))
            return redirect('login')


    return render(request,'login.html',{'nbar': 'login','next':next} )

def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        form2 = RegisterUserInfoForm(request.POST)
        if form.is_valid():
            if form2.is_valid():
                user=form.save()
                Info=form2.save(commit=False)
                Info.user = user
                Info.save()
                return redirect('home')
    else:
        form = RegisterUserForm()
        form2 = RegisterUserInfoForm()

    return render(request,'register.html',{'register_form':form,'register_form2':form2})

def contact_us_view(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,_('Contact message was send succesfuly'))
            return redirect('contact_us')
    else:
        form = ContactUsForm()



    return render(request,'contact_us.html',{'form':form})


def doctors(request):

    User=get_user_model()
    user = UserInfo
    Specialist = request.GET.get('Specialist')
    city = request.GET.get('city')
    area = request.GET.get('area')
    name = request.GET.get('name')
    try :
        Specialist = int(Specialist)
        city = int(city)
        area = int(area)
    except :
        pass

    filters = {'is_doctor':True}
    if (Specialist  and   Specialist != 0) :
        filters['specialty__pk'] = Specialist

    if ( city and city!=0 ):
        filters['address__city__pk'] = city

    if (area and area!=0 ):
        filters['address__pk'] = area

    if (name and name!="" ):
        filters['full_name__icontains'] = name

    doctors = user.objects.all().annotate(full_name=Concat('user__first_name'  ,Value(' '),'user__last_name'))
    doctors = doctors.select_related('user').filter( **filters).order_by('user__first_name')
    paginator = Paginator(doctors, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    Specialties = Specialty.objects.all()
    Cities = City.objects.all()
    return render(request,'doctors.html',{'page_obj':page_obj,'Specialties':Specialties,'Cities':Cities })


def get_modelAPI(request,id):
    ar = Area.objects.all().filter(city__pk = id)
    json_result = serializers.serialize('json',ar)
    return HttpResponse(json_result, content_type="application/json")

@login_required
def patient_file(request):
    patient = UserInfo.objects.get(user__pk = request.user.id)
    patient_registers = PatientRegister.objects.all().filter(patient__user__pk = request.user.id)
    patient_chronic_conditions = patient.chronic_conditions.all()
    return render(request,'patient_file.html',{'patient':patient ,'PCCs':patient_chronic_conditions,'patient_registers':patient_registers})

@login_required
def d_to_patient_file(request,id):

    patient = UserInfo.objects.get(user__pk = id)
    patient_registers = PatientRegister.objects.all().filter(patient__user__pk = patient.id)
    patient_chronic_conditions = patient.chronic_conditions.all()
    return render(request,'patient_file.html',{'patient':patient ,'PCCs':patient_chronic_conditions,'patient_registers':patient_registers})


def doctor_book(request,id):
    doctor = UserInfo.objects.get(user__pk=id)
    off_day = doctor.off_day.all().values()

    return render(request,'doctor_book.html',{'off_day':off_day ,'doctor':doctor})

def get_appointment(request,id,apdate):
    appointment = Appointment.objects.filter(doctor__user__pk =id ).exclude(status=3).order_by('time_from')
    doctor = UserInfo.objects.get(user__pk=id)
    if doctor.start_time and doctor.end_time:
        start = doctor.start_time
        end = doctor.end_time
    else :
        start = time(0,0)
        end = time(0,0)
    whileEnd = datetime.combine(apdate, start)
    available_appointment = []
    bool_appointment = True
    if not appointment :
        while (whileEnd < (datetime.combine(apdate, end) - timedelta(minutes=15))):
            available_appointment.append({'start':whileEnd.time(),'end':(whileEnd + timedelta(minutes=15)).time()})
            whileEnd = whileEnd + timedelta(minutes=15)

    else :
        while (whileEnd < (datetime.combine(apdate, end) - timedelta(minutes=15))):
            for a in appointment:
                if (datetime.combine(apdate, a.time_from)<= whileEnd and datetime.combine(apdate, a.time_to)> whileEnd)  or ( datetime.combine(apdate, a.time_from)>= whileEnd  and datetime.combine(apdate, a.time_from)< (whileEnd + timedelta(minutes=15)) ) or ((datetime.now()+ timedelta(minutes=60) )>(whileEnd )) :
                    bool_appointment = False
                    break
            if bool_appointment :
                available_appointment.append({'start':whileEnd.time(),'end':(whileEnd + timedelta(minutes=15)).time()})
            bool_appointment = True
            whileEnd = whileEnd + timedelta(minutes=15)
    return JsonResponse({ 'available_appointment':available_appointment}, content_type="application/json")

@login_required
def patient_appointments(request):

    if request.GET.get('old') :
        old = request.GET['old']
        if str(old).lower() == 'true':
            patient_appointments = Appointment.objects.filter(Q(adate__lt=date.today() )|(Q(adate=date.today() )& Q(time_from__lt=datetime.now().time())),patient__user__pk=request.user.id )
        else :
            patient_appointments = Appointment.objects.filter(Q(adate__gte=date.today() )|(Q(adate=date.today() )& Q(time_from__gte=datetime.now().time())),patient__user__pk=request.user.id )
    else:
        patient_appointments = Appointment.objects.filter(Q(adate__gte=date.today() )|(Q(adate=date.today() )& Q(time_from__gte=datetime.now().time())),patient__user__pk=request.user.id )
    return render(request,'patient_appointments.html',{'patient_appointments':patient_appointments})

@login_required
def book_appointment(request,doctor_id):
    doctor = UserInfo.objects.get(user__pk=doctor_id)
    patient = UserInfo.objects.get(user__pk=request.user.id)
    ## if method post added
    if request.method=='POST':
        request.POST
        r=request.POST.copy()
        r['doctor']=  doctor
        r['patient'] = patient

        form = AppointmentForm(r)
        if form.is_valid():
            a=Appointment.objects.filter((Q(time_from__gte=form.cleaned_data['time_from']) & Q(time_from__lt=form.cleaned_data['time_to']) )| (Q(time_from__lte=form.cleaned_data['time_from']) & Q(time_to__gt=form.cleaned_data['time_from'])),patient__pk=patient.id,adate=form.cleaned_data['adate'])
            if(a):
                messages.error(request, _('You have a conflicting date'))
                return redirect(doctor_book,doctor_id)   
            else :
                form.save()
                messages.success(request,_('appointment was booked successfully'))
        else :
            messages.error(request,_('information not completed'))
            return redirect(doctor_book,doctor_id )

    return redirect(patient_appointments)

@login_required
def doctor_appointment(request):
    page = 0
    Page_position =0
    if request.method =='POST':
        Page_position = request.POST.get('position')
        page = request.POST.get('page')
        edit_appointment = Appointment.objects.get(id=request.POST.get('id'))
        if (request.POST.get('_method').upper() == 'PUT'):
            if edit_appointment.status == 2:
                if (request.POST.get('status').lower() == 'reject') :
                    edit_appointment.status = 3
                    edit_appointment.save()
                    messages.success(request,_("appointment was rejected"))
        
                elif (request.POST.get('status').lower() == 'accept') :
                    edit_appointment.status = 1
                    edit_appointment.save()
                    messages.success(request,_("appointment was accepted"))
                else :
                    messages.warning(request,_("can't change to this status"))

            elif (edit_appointment.status == 3 or edit_appointment.status == 1 ):
                    if (request.POST.get('status').lower() == 'not_attended'):
                        edit_appointment.status = 5
                        edit_appointment.save()
                        messages.success(request,_("Appointment status changed to not attended"))
                    else :
                        messages.warning(request,_("can't change to this status"))
            else :
                messages.warning(request,_("can't change to this status"))


    if (not Page_position):
        Page_position=0
    if (not page):
        page = 0
    doctor_appointments = Appointment.objects.filter(doctor__user__pk=request.user.id )


    return render (request,'doctor_appointment.html',{'doctor_appointments':doctor_appointments,'position':Page_position, 'page':page })


@login_required
def doctor_dashboard(request):

    return render(request, 'doctor_dashboard.html')

@login_required
def work_time(request):
    if request.method == 'POST':
            doctor = User.objects.get( id = request.user.id)
            
            form=Worktime(request.POST)
            
            if form.is_valid():
                selected_days = []
                
                for q in  form.cleaned_data['off_day'] :
                    s = Day.objects.get(value=q.value)
                    selected_days.append(s)
             
                doctor.Info.start_time =  form.cleaned_data['start_time']
                doctor.Info.end_time = form.cleaned_data['end_time']
                doctor.Info.off_day.clear()
                doctor.Info.off_day.add(*selected_days)
                doctor.Info.save()

    days = dict.fromkeys(['Monday' ,'Tuesday' ,'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    off_day = request.user.Info.off_day.all()
    start_time = request.user.Info.start_time
    end_time =request.user.Info.end_time
    a=[]
    for d in off_day :
        a.append(d.day)
    
    for key , val in days.items():
    
        if key in a :
            days[key] = True
        else :
            days[key] = False
        
    return render(request, 'work_time.html',context={'JS_off_days':json.dumps( days),'off_days':days,'start_time':start_time,'end_time':end_time})


@login_required
def attendace(request,appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    if appointment.doctor == request.user.Info :
        if appointment.status == 1 :
            if request.method == 'POST':
                patientReg = PatientRegisterForm(request.POST,request.FILES )
                
                if patientReg.is_valid :
                    instance = patientReg.save(commit=False)
                    instance.doctor = appointment.doctor
                    instance.patient = appointment.patient
                    appointment.status = 4 
                    appointment.save()
                    instance.save()
                    messages.success(request,_('Information was added'))
                    return redirect('doctor_appointment')
            form = PatientRegisterForm()
            return render(request,'attendace.html',{'form':form ,'appointment_id':appointment_id})
        else :
            messages.warning(request,_('Appointment status should be accepted'))
            return redirect('doctor_appointment')
    else :
        return redirect('home')

