from datetime import date

from .models import Activity, Property
from rest_framework import serializers


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ["id", "title", "address"]


today = date.today()


class ActivitySerializer(serializers.ModelSerializer):
    property_id = PropertySerializer(read_only=True)  # True, no sale para llenar
    # tracks = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='track-detail'
    # )

    # created_at = serializers.CreateOnlyDefault(default=today) #CreateOnlyField()
    # schedule = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    property = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), source="property_id",write_only=True)
    condition = serializers.SerializerMethodField('evaluar_condiciones')

    def evaluar_condiciones(self, foo):
        if foo.status == "active" and foo.schedule.date() >= today:
            return "Pendiente a realizar"
        elif foo.status == "active" and foo.schedule.date() < today:
            return "Atrasada"
        elif foo.status == "done":
            return "Finalizada"
        else:
            return ""

    class Meta:
        model = Activity
        exclude = ["updated_at"]
        read_only_fields = ('created_at',)
