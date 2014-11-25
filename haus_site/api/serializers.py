from django.contrib.auth.models import User, Group
from rest_framework import serializers


class DeviceSerializer(serializers.Serializer):
    pk = serializers.Field()
    name = serializers.CharField(max_length=100)
    atoms = serializers.SerializerMethodField('get_atoms')

    def get_atoms(self, obj):
        return [atom.name for atom in obj.atoms.all()]
