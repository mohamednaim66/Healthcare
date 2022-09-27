from cProfile import label
from dataclasses import field
import email
from logging import PlaceHolder
from tkinter import Widget
import django
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _
from main.models import Appointment, Contact_message, Day, PatientRegister, UserInfo
from django.utils.translation import get_language_bidi


class RegisterUserForm(UserCreationForm):
    
    

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':_('Username')}),
            'email': forms.TextInput(attrs={'class':'form-control ','placeholder':_('Email') }),
            'first_name': forms.TextInput(attrs={'class':'form-control ','placeholder':_('first name')}),
            'last_name': forms.TextInput(attrs={'class':'form-control ','placeholder':_('last name')}),


        }
        help_texts = {
            'email': _('Your email must be like example@gmail.com')
        }
        
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm,self).__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({'class':'form-control','placeholder':_('Password')}) 
        self.fields["password2"].widget.attrs.update({'class':'form-control','placeholder':_('Password confirmation')}) 


           

class RegisterUserInfoForm(forms.ModelForm):
     class Meta:
        model = UserInfo
        fields = ('PhoneNum',)
        widgets = {
            'PhoneNum': forms.TextInput(attrs={'class':'form-control','placeholder':_('Phone Number')}),
            }
        labels ={
            'PhoneNum' : _('Phone number') 
     
        }
       


class Worktime(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('start_time','end_time','off_day')

    def __init__(self, *args, **kwargs):
        super(Worktime,self).__init__(*args, **kwargs)
        self.fields["off_day"].to_field_name = "value"
       
        
       

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('doctor','patient','adate','time_from','time_to')
       

class ContactUsForm(forms.ModelForm):
     class Meta:
        model = Contact_message
        fields = ('name','email','subject','message')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':_('Your name')}),
            'email': forms.TextInput(attrs={'class':'form-control','placeholder':_('Email')}),
            'subject': forms.TextInput(attrs={'class':'form-control','placeholder':_('Message subject')}),
            'message': forms.Textarea(attrs={'class':'form-control','placeholder':_('Message content'),'style':' resize: none; height: 134px;'}),

            }
        labels ={
            'name' :_('Name'),
            'email' :_('Email'),
            'subject' :_('Subject'),
            'message' :_('Message'),
        }

class PatientRegisterForm(forms.ModelForm):
    class Meta: 
        model = PatientRegister
         
        fields = ('type','file','discrption')
        widgets ={
            'discrption': forms.Textarea(attrs={'class':'form-control col-12','placeholder':_('Discrption')}),
            'file': forms.FileInput(attrs={'class':'form-control col-12','placeholder':_('File')}),
            'type': forms.TextInput(attrs={'class':'form-control col-12','placeholder':_('Type of appointment')}),
        }
        labels = { 
            'discrption': _('Discrption'),
            'file': _('File'),
            'type': _('Type'),
        }

       


