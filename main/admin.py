from django.contrib import admin
from django.contrib.auth.models import User
from main import models

# Register your models here.


@admin.register(models.UserInfo)
class InfoAdmin(admin.ModelAdmin):
    list_display = ("user", "PhoneNum",'is_doctor' ,'address' , 'gender' , 'birth_date')


@admin.register(models.Contact_message)
class Contact_messageAdmin(admin.ModelAdmin):
    list_display = ('name','email','subject','message','date')
    

@admin.register(models.Specialty)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('name','image')
    
@admin.register(models.Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title','doctor','info','start_price')
     
@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    
@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id','name','city')

@admin.register(models.PatientRegister)
class PatientRegisterAdmin(admin.ModelAdmin):
    list_display = ('id','doctor','patient','register_date','type','discrption','filename' )
    
@admin.register(models.Chronic_condition)
class Chronic_conditionAdmin(admin.ModelAdmin):
    list_display = ('name',)
      
@admin.register(models.Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor','patient','adate','time_from','time_to',)

@admin.register(models.Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('day','value',)