from rest_framework import serializers

from accounts.models import StaffMember
from meetings.models import Meeting
from subjects.models import Subject


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMember
        fields = ['email', 'given_name', 'surname']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['index', 'type', 'category', 'collective_body_id']


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['index', 'collective_body_id']
