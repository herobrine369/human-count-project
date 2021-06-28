from rest_framework import serializers

from .models import PersonsCount


class PersonsCountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PersonsCount
        fields = ['time', 'count']
