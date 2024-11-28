from django.shortcuts import render
from .models import Orendsrs, Rooms, Renta
from django.http import JsonResponse

def show_tables(request):
    tables = {
        "Orendsrs": Orendsrs.objects.all(),
        "Rooms": Rooms.objects.all(),
        "Renta": Renta.objects.select_related('id_orendsrs', 'id_number_rooms').all(),
    }
    for table_name, rows in tables.items():
        print(f"{table_name}: {len(rows)} rows")
    return render(request, 'storinka.html', {'tables': tables})



def debug_tables(request):
    tables = {
        "Orendsrs": list(Orendsrs.objects.values()),
        "Rooms": list(Rooms.objects.values()),
        "Renta": list(Renta.objects.values('date_start', 'count_days', 'goal_rental', 'id_orendsrs__name_firm', 'id_number_rooms__area')),
    }
    return JsonResponse(tables)
