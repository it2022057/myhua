from django.db.models import Max
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import StaffMember
from meetings.models import Meeting
from subjects.models import Subject
from .permissions import IsSecretariatUser
from .serializers import StaffSerializer, SubjectSerializer, MeetingSerializer


# Create your views here.


"""
Generic API view that filters objects using one query parameter
"""


class CustomApiView(APIView):
    model = None
    serializer_class = None
    query_param = None
    filter_field = None
    missing_param_message = 'Missing the collective body param.'

    def get(self, request, *args, **kwargs):
        param_value = request.query_params.get(self.query_param)

        if not param_value:
            return Response({'detail': self.missing_param_message}, status=status.HTTP_400_BAD_REQUEST)

        filter_kwargs = {self.filter_field: param_value}

        objects = self.model.objects.filter(**filter_kwargs)
        serializer = self.serializer_class(objects, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


"""
Generic API view that returns the next available index
"""


class NextIndexApiView(CustomApiView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsSecretariatUser]
    query_param = 'collective_body_id'
    filter_field = 'collective_body_id'

    def get(self, request, *args, **kwargs):
        param_value = request.query_params.get(self.query_param)

        if not param_value:
            return Response({'detail': self.missing_param_message}, status=status.HTTP_400_BAD_REQUEST)

        filter_kwargs = {self.filter_field: param_value}

        previous_index = (
                self.model.objects
                .filter(**filter_kwargs)
                .aggregate(max_index=Max('index'))['max_index']
                or 0
        )

        return Response({'next_index': previous_index + 1}, status=status.HTTP_200_OK)


"""
API views that return filtered model objects as JSON
"""


class StaffMemberApiView(CustomApiView):
    model = StaffMember
    serializer_class = StaffSerializer
    query_param = 'email'
    filter_field = 'email'
    missing_param_message = 'Missing the email param.'


class SubjectApiView(CustomApiView):
    model = Subject
    serializer_class = SubjectSerializer
    query_param = 'collective_body_id'
    filter_field = 'collective_body_id'


class MeetingApiView(CustomApiView):
    model = Meeting
    serializer_class = MeetingSerializer
    query_param = 'collective_body_id'
    filter_field = 'collective_body_id'


"""
Views that return the next index of a collective body's subject or meeting
"""


class SubjectNextIndexApiView(NextIndexApiView):
    model = Subject


class MeetingNextIndexApiView(NextIndexApiView):
    model = Meeting
