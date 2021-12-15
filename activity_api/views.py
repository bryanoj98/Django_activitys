from datetime import date
import datetime

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .models import Activity, Property
from rest_framework import viewsets
from .serializers import ActivitySerializer
from .forms import ActivityForm

today = date.today()


class ActivityViewset(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        actividades = Activity.objects.all()
        filter_status = self.request.GET.get('status')
        filter_start = self.request.GET.get('start')
        filter_end = self.request.GET.get('end')
        filter_id = self.kwargs.get('pk')
        default_filter = True

        if filter_status:
            try:
                actividades = actividades.filter(status=filter_status)
                default_filter = False
            except:
                print("Error: El parametro status, no tiene un valor valido para el filtrado")

        if filter_start and filter_end:
            try:
                actividades = actividades.filter(
                    schedule__range=(filter_start, filter_end))
                default_filter = False
            except:
                print("Error: Los parametros de rango schedule, no tienen un valores validos para el "
                      "filtrado")

        elif filter_start and filter_end is None:
            try:
                actividades = actividades.filter(schedule__gte=filter_start)
                default_filter = False
            except:
                print("Error: El parametro start, no tiene un valor valido para el filtrado")

        elif filter_end and filter_start is None:
            try:
                actividades = actividades.filter(schedule__lte=filter_end)
                default_filter = False
            except:
                print("Error: El parametro end, no tiene un valor valido para el filtrado")

        if default_filter and filter_id is None:
            actividades = actividades.filter(
                schedule__range=(today - datetime.timedelta(days=3), today + datetime.timedelta(weeks=2)))

        return actividades

    def create(self, request, *args, **kwargs):
        data = request.data
        property = Property.objects.filter(id=data['property']).first()

        if property.status == "disable":
            return Response({"Error": "Propiedad desactivada"})

        schedule_data = datetime.datetime.strptime(data['schedule'].replace('T', ''), "%Y-%m-%d%H:%M")

        cruce_actividades = Activity.objects.filter(
            schedule__range=(
                schedule_data - datetime.timedelta(minutes=59), schedule_data + datetime.timedelta(minutes=59)))
        if cruce_actividades:
            return Response({"Error": "Existen actividades previas asignadas a la propiedad dentro del rango horario"})

        new_Activity = Activity.objects.create(property_id=property, schedule=data['schedule'],
                                               title=data['title'], created_at=datetime.datetime.now(),
                                               updated_at=datetime.datetime.now(), status=data['status'])
        new_Activity.save()
        serializer_context = {
            'request': request,
        }
        serializer = ActivitySerializer(new_Activity, context=serializer_context)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = request.data
        if data["status"] == "cancel":
            return Response({"Error": "No se pueden re-agendar actividades canceladas."})

        activity_object = Activity.objects.get(id=kwargs['pk'])
        activity_object.schedule = data["schedule"]
        activity_object.updated_at = datetime.datetime.now()
        activity_object.save()

        serializer_context = {
            'request': request,
        }
        serializer = ActivitySerializer(activity_object, context=serializer_context)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        activity_object = Activity.objects.get(id=kwargs['pk'])
        activity_object.status = "cancel"
        activity_object.save()

        serializer_context = {
            'request': request,
        }
        serializer = ActivitySerializer(activity_object, context=serializer_context)
        return Response(serializer)


# Create your views here.
def home(request):
    return render(request, 'home.html')


def activity(request):
    data = {
        'form': ActivityForm()
    }
    if request.method == 'POST':
        formulario = ActivityForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Guardado exitoso"
        else:
            data["form"] = formulario
            data["mensaje"] = "Error en los datos ingrasados"

    return render(request, 'activity.html', data)
