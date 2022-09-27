
from datetime import datetime
from django.contrib.auth import get_user_model
from main.models import Appointment, UserInfo

def top_products(request):
    if( request.user.is_authenticated ):
        User = get_user_model()
        today_date = datetime.now().date()
        time = datetime.now().time()

        if request.user.Info.is_doctor :
            upAppointment = Appointment.objects.filter(doctor__pk = request.user.Info.id ,adate = today_date , time_from__gt = time  ).count()
        else : 
            upAppointment = Appointment.objects.filter(patient__pk = request.user.Info.id , adate = today_date , time_from__gt = time).count()

        user = User.objects.get(pk = request.user.id)
        userInfo =UserInfo.objects.get(user=user)
        return {'userInfo':userInfo ,'upAppointment':upAppointment} # of course some filter here
    return {}

