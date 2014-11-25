from django.contrib.auth.models import User, Group
from api.models import TimeSeries
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class DeviceSerializer(serializers.Serializer):
    pk = serializers.Field()
    name = serializers.CharField(max_length=100)
    atoms = serializers.SerializerMethodField('get_atoms')

    def get_atoms(self, obj):
        return [atom.name for atom in obj.atoms.all()]



# class TimeSeriesSerializer(serializers.Serializer):
#     pk = serializers.Field()
#     value = serializers.DecimalField()
#     owner = serializers.Field(source='owner.username')

#     def restore_object(self, attrs, instance=None):
#         if instance:
#             instance.value = attrs.get('value', instance.value)
#             return instance
#         return TimeSeries(attrs)

