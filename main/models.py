from ast import Delete
from asyncio.windows_events import NULL
from datetime import date, datetime
from distutils.command.sdist import sdist
from email.headerregistry import Address
from email.policy import default
from functools import partial
from msilib.schema import Class
from multiprocessing.sharedctypes import Value
from operator import mod
import os
from random import choice
from tkinter import CASCADE
from unicodedata import name
from wsgiref.validate import validator
from django.conf import settings
from django.db import models
from PIL import Image
from django.core.validators import RegexValidator
from django.core.files.images import get_image_dimensions
import uuid
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
# Create your models here.





class Contact_message(models.Model):
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=70)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(default=datetime.now,blank=True)

class Chronic_condition(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name 

class History_type(models.Model):
    type = models.CharField(max_length=50)

class Specialty (models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Specialist')
    def __str__(self):
        return self.name 
  
def validate_image(image):
    min_height = 300
    min_width = 300
    (width, height) = get_image_dimensions(image.file)
    
    if width < min_width or height < min_height:
        raise ValidationError(_("Height or Width is smaller than what is allowed"))

    if width != height :
        raise ValidationError(_("Height and Width is not equal"))
  
class City(models.Model):
    name = models.CharField(max_length=100,verbose_name='City')
    def __str__(self) :
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=100 , verbose_name='Area')
    city = models.ForeignKey(City ,on_delete = models.CASCADE , null = False , blank = False)
    def __str__(self) :
        return (self.name +", "+self.city.name)

class Day(models.Model):
    day = models.CharField(max_length=20, null=False, blank=False)
    value =  models.IntegerField(null=False, blank=False,unique=True)
    def __str__(self) :
        return (self.day)
    
   
class UserInfo(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='Info'
        )
    PhoneNum = models.CharField(verbose_name="Phone number",max_length=12, validators=[ RegexValidator(
            regex='^05[0-9]{8}$',
            message=_('Phone number must start 05 and it 10 digit like 05xxxxxxxx'),
            code='invalid_password'
        ),])
    is_doctor = models.BooleanField(default=False)
    specialty = models.ForeignKey(
                Specialty ,
                on_delete=models.CASCADE,
                null=True ,
                blank=True
                )
    image_profile = models.ImageField(upload_to = 'Images_profile', default='Images_profile/default_profile.jpg' , null=True , blank=True ,  validators=[validate_image])
    address = models.ForeignKey(
        Area,
        on_delete = models.CASCADE,
        null = True ,
        blank = True
    )
    ex_address = models.CharField(max_length=200,null=True ,blank=True)
    gender = models.CharField(max_length = 10, null = True , blank = True )
    birth_date = models.DateField( null=True,blank=True)
    chronic_conditions = models.ManyToManyField(Chronic_condition , blank = True)
    start_time = models.TimeField( null = True , blank = True )
    end_time = models.TimeField( null = True , blank = True )
    off_day = models.ManyToManyField(Day,  blank = True ,related_name='off_days')

    @property
    def age(self):
        if(self.birth_date):
            return int((datetime.now().date() - self.birth_date).days / 365)
        else :
            return ''

    def __unicode__(self):
        return "{0}".format(self.image_profile)

    def __str__(self) -> str:
        return self.user.username

    def save(self):
        if not self.image_profile:
            return        
                
        super(UserInfo, self).save() 
        image = Image.open(self.image_profile)
        (width, height) = image.size     
        size = ( 300, 300)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.image_profile.path)

class Offer(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    title = models.CharField(max_length=50)
    info = models.CharField(max_length=100)
    start_price = models.IntegerField()
    end_price = models.IntegerField()

@deconstructible
class random_name(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self,instance,filename):
        ext=filename.split('.')[-1]
        filename='{}.{}'.format(uuid.uuid4().hex,ext)
        return os.path.join(self.path , filename)
    
        
class PatientRegister(models.Model):
    doctor = models.ForeignKey(
        UserInfo,
        on_delete = models.CASCADE,
        null=True,
        blank=True,
        related_name='doctor'
    )
    patient = models.ForeignKey(
        UserInfo,
        on_delete = models.CASCADE,
        null=True,
        blank=True,
        related_name='patient'
    )
    register_date = models.DateTimeField(auto_now_add = True , blank = True)
    type = models.CharField(max_length=50)
    discrption = models.TextField()
    file = models.FileField(upload_to = random_name('Files'))
    
    @property
    def filename(self):
       return os.path.basename(self.file.name)

class Appointment(models.Model):
    status_choices= [
        (1,'accepted'),
        (2,'pended'),
        (3,'rejected'),
        (4,'Attended'),
        (5,'Not attended'),

    ]
    doctor = models.ForeignKey(
        UserInfo,
        on_delete = models.CASCADE,
        null=True,
        blank=True,
        related_name='doctor_appointment_set'
    )
    patient = models.ForeignKey(
        UserInfo,
        on_delete = models.CASCADE,
        null=True,
        blank=True,
        related_name='patient_appointment_set'
    )
    adate = models.DateField() 
    time_from = models.TimeField()
    time_to = models.TimeField()
    status = models.IntegerField( choices=status_choices ,default=2,blank=True)

    def __str__(self) -> str:
        return str(self.time_from)+str(self.time_to)+" : "  +str(self.adate) + " : " +self.get_status_display()




    


    
    
    
    
    