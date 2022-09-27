from django.utils.translation import gettext as _ 
from django import template


register = template.Library()


@register.filter(name='dayStr')
def dayStr(value):
    if value == 'Monday':
        return _('Monday')
    elif value == 'Tuesday':
        return _('Tuesday')
    elif value == 'Wednesday':
        return _('Wednesday')
    elif value == 'Thursday':
        return _('Thursday')
    elif value == 'Friday':
        return _('Friday')
    elif value == 'Saturday':
        return _('Saturday')
    elif value == 'Sunday':
        return _('Sunday')
    else :
        return None


@register.filter(name='dayVal')
def dayVal(value):
    if value == 'Monday':
        return 1
    elif value == 'Tuesday':
        return 2
    elif value == 'Wednesday':
        return 3
    elif value == 'Thursday':
        return 4
    elif value == 'Friday':
        return 5
    elif value == 'Saturday':
        return 6
    elif value == 'Sunday':
        return 0
    else :
        return None
    
    