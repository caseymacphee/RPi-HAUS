from django.contrib.auth.models import User, Group
from rest_framework import serializers
from haus.models import Device, Atom, Data, CurrentData


class AtomSerializer(serializers.ModelSerializer):

    class Meta:

        model = Atom




    def restore_object(self, attrs, instance=None):

        print("attrs == " + str(attrs))

        # print str(instance)

        if instance:

            instance.atom_name = attrs.get('atom_name', instance.atom_name)
            instance.device = attrs.get('device', instance.device)

            instance.save()
            return instance

        return Atom(**attrs)



class DataSerializer(serializers.ModelSerializer):

    atom_name = serializers.SerializerMethodField('get_atom_name')

    def get_atom_name(self, obj):
        return obj.atom.atom_name

    class Meta:
        model = Data

    # def restore_object(self, attrs, instance=None):

    #     # Instance should never exist when submitting data through the API.
    #     # if instance:

    #     #     instance.atom = attrs.get('atom', instance.atom)
    #     #     instance.value = attrs.get('value', instance.value)
    #     #     instance.timestamp = attrs.get('timestamp', instance.timestamp)

    #     #     instance.save()
    #     #     return instance
    #     print(str(attrs))
    #     return Data(**attrs)


class CurrentDataSerializer(serializers.ModelSerializer):
    
    atom_name = serializers.SerializerMethodField('get_atom_name')

    def get_atom_name(self, obj):
        return obj.atom.atom_name

    class Meta:
        model = CurrentData

    def restore_object(self, attrs, instance=None):

        if instance:

            # For current data, the atom will never
            # change once it has been assigned.
            # instance.atom = attrs.get('atom', instance.atom)
            instance.value = attrs.get('value', instance.value)
            instance.timestamp = attrs.get('timestamp', instance.timestamp)

            instance.save()
            return instance

        print(str(attrs))
        return CurrentData(**attrs)


# class DataSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Data



class DeviceSerializer(serializers.ModelSerializer):
    # id = serializers.Field()
    # name = serializers.CharField(max_length=200)
    atoms = serializers.SerializerMethodField('get_atoms')

    # NOTE: Devices currently only have one user.
    # If this changes, see also the models.py file and views.py file.
    # ForeignKey for serializers is RelatedField. Reference:
    # http://www.django-rest-framework.org/api-guide/relations/
    # user = serializers.PrimaryKeyRelatedField()
    # user = serializers.RelatedField()

    # 'monitor' or 'controller'
    # device_type = serializers.CharField(max_length=20)

    # serialpath might not be on Devices -- maybe move to AtomSerializer
    # depending on what the model turns out to be?
    # serialpath = serializers.CharField(max_length=200)

    # user = serializers.SerializerMethodField('get_user_id')

    # def get_user_id(self, obj):
    #     return obj.user.pk

    class Meta:
        model = Device

    def get_atoms(self, obj):
        return {atom.atom_name: atom.pk for atom in obj.atoms.all()}

    # Requires importing the models (so you can create a new entry in the DB)

    def restore_object(self, attrs, instance=None):

        print("attrs == " + str(attrs))

        print str(instance)

        if instance:
            self.was_created = False
            instance.device_name = attrs.get('device_name', instance.device_name)
            instance.user = attrs.get('user_id', instance.user)
            instance.device_type = attrs.get('device_type', instance.device_type)

            instance.save()
            return instance

        self.was_created = True

        return Device.create(**attrs)













