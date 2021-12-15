from datetime import date, datetime

from .models import Activity, Property, Survey
from rest_framework import serializers

today = date.today()


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ["id", "title", "address"]


class ActivitySerializer(serializers.HyperlinkedModelSerializer):
    property_id = PropertySerializer(read_only=True)
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), source="property_id",
                                                  write_only=True)
    condition = serializers.SerializerMethodField('evaluar_condiciones')

    def evaluar_condiciones(self, foo):
        try:
            schedule_data = foo.schedule.date()
        except:
            schedule_data = datetime.strptime(foo.schedule.replace('T', ''), "%Y-%m-%d%H:%M:%S").date()
        if foo.status == "active" and schedule_data >= today:
            return "Pendiente a realizar"
        elif foo.status == "active" and schedule_data < today:
            return "Atrasada"
        elif foo.status == "done":
            return "Finalizada"
        else:
            return ""

    class Meta:
        model = Activity
        exclude = ["updated_at"]
        read_only_fields = ('created_at',)
