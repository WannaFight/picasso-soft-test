from rest_framework import serializers

from police_reports.models import Crime


class CrimeSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Crime
