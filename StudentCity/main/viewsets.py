from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Dormitory, Rooms, Student
from .permissions import UserPermission
from .serializers import (StudentSerializer, StudentDetailSerializer,
                          DormitorySerializer, RoomSerializer)
from .utils import StudentAPIPagination


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('room__dorm', 'owner').order_by('last_name', 'first_name', 'id')
    pagination_class = StudentAPIPagination
    permission_classes = (UserPermission,)

    def get_queryset(self):
        queryset = super().get_queryset()
        room = self.request.query_params.get('room')
        if room is not None:
            if room.isdigit():
                queryset = queryset.filter(room_id=room)
            else:
                queryset = queryset.none()
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StudentDetailSerializer
        return StudentSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DormitoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dormitory.objects.order_by('id')
    serializer_class = DormitorySerializer

    @action(detail=True, methods=['get'])
    def rooms(self, request, pk=None):
        dorm = self.get_object()
        rooms = Rooms.objects.filter(dorm=dorm).prefetch_related('facilities').order_by('id')
        return Response(RoomSerializer(rooms, many=True).data)


class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rooms.objects.select_related('dorm').prefetch_related('facilities').order_by('id')
    serializer_class = RoomSerializer

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        room = self.get_object()
        students = Student.objects.filter(room=room).order_by('last_name', 'first_name')
        serializer = StudentSerializer(students, many=True, context=self.get_serializer_context())
        return Response(serializer.data)
