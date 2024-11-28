from django.shortcuts import render
from .models import Orendsrs, Rooms, Renta


def index(request):
    context = {
        'project_title': 'Rental Project',
        'student_info': {'Імя': 'Скоробогата Людмила', 'Група': 'КН-21003б'},
        'tables': {
            'Orendsrs': Orendsrs.objects.all(),
            'Rooms': Rooms.objects.all(),
            'Renta': Renta.objects.all(),
        }
    }
    return render(request, 'storinka.html', context)