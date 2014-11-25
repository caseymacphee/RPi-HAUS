from django.contrib.auth.models import User, Group
from rest_framework import serializers


class DeviceSerializer(serializers.Serializer):
    pk = serializers.Field()
    name = serializers.CharField(max_length=200)
    atoms = serializers.SerializerMethodField('get_atoms')

    # NOTE: Devices currently only have one user.
    # If this changes, see also the models.py file and views.py file.
    # ForeignKey for serializers is RelatedField. Reference:
    # http://www.django-rest-framework.org/api-guide/relations/
    user = serializers.RelatedField()

    # 'monitor' or 'controller'
    device_type = serializers.CharField(max_length=20)

    # serialpath might not be on Devices -- maybe move to AtomSerializer
    # depending on what the model turns out to be?
    serialpath = serializers.CharField(max_length=200)

    def get_atoms(self, obj):
        return [atom.name for atom in obj.atoms.all()]

    # Requires importing the models (so you can create a new entry in the DB)

    def restore_object(self, attrs, instance=None):

        if instance:

            instance.name = attrs.get('name', instance.name)
            instance.serialpath = attrs.get('serialpath', instance.serialpath)
            instance.user = attrs.get('user', instance.user)
            instance.device_type = attrs.get('device_type', instance.device_type)
            instance.save()
            return instance

        return Device(**attrs)













