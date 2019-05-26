from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import BoxesSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from .models import Box, InventoryConditions
import django_filters
from .customfilters import BoxFilters, BoxUserFilters
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from rest_framework.views import APIView


def check_box_threshold(request):
    """
    Conditions to be fulfilled on each add/update/delete:
    Average area of all added boxes should not exceed A1
    Average volume of all boxes added by the current user shall not exceed V1
    Total Boxes added in a week cannot be more than L1
    Total Boxes added in a week by a user cannot be more than L2

    Values A1, V1, L1 and L2 shall be configured externally.
    You can choose 100, 1000, 100, and 50 as their respective default values.
    """

    length = int(request.data['length'])
    width = int(request.data['width'])
    height = int(request.data['height'])

    area = 2 * (length * width + width * height + height * length)
    volume = length * width * height

    inventory_condition = InventoryConditions.objects.all()
    if inventory_condition:
        average_area_thresold = inventory_condition[0].average_area
        average_volume_thresold = inventory_condition[0].average_area
        total_boxes_thresold = inventory_condition[0].total_boxes

    sum_area = Box.objects.all().aggregate(Sum('area'))['area__sum']
    count_box = Box.objects.count()

    new_avg_area = (sum_area + area) / count_box + 1

    if new_avg_area > average_area_thresold:
        return Response({'details': 'average area can not be greater then {}'.format(average_volume_thresold)})

    sum_volume = Box.objects.all().aggregate(Sum('volume'))['volume__sum']
    new_avg_volume = (sum_volume + volume) / count_box + 1

    if new_avg_volume > average_volume_thresold:
        return Response({'details': 'average volume can not be greater then {}'.format(average_volume_thresold)})

    some_day_last_week = (timezone.now() - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    total_box = Box.objects.filter(Q(created_at__gte=some_day_last_week) & Q(created_at__gte=today)).count()

    if total_box > total_boxes_thresold:
        return Response({'details': 'Total number of box has reach the limit for this week'.
                        format(total_boxes_thresold)}, status=status.HTTP_200_OK)


class ListCreateBox(generics.ListCreateAPIView):
    queryset = Box.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = BoxFilters

    serializer_class = BoxesSerializer

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        is_staff = request.user.is_staff
        exclude_fields = ()
        if is_staff:
            exclude_fields = (
                "created_at",
                "updated_at"
            )

        serializer = self.get_serializer(queryset, many=True, exclude_fields=exclude_fields)

        return Response(serializer.data)

    def post(self, request, format=None):
        request.POST._mutable = True
        user_id = request.user.id
        length = int(request.data['length'])
        width = int(request.data['width'])
        height = int(request.data['height'])
        area = 2 * (length * width + width * height + height * length)
        volume = length * width * height
        request.data['volume'] = volume
        request.data['area'] = area
        request.data['created_by'] = user_id
        request.data['updated_by'] = user_id

        response = check_box_threshold(request)
        if response is not None:
            return response

        serializer = BoxesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateBoxView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    # http_method_names = ['DELETE', 'put']
    queryset = Box.objects.all()
    serializer_class = BoxesSerializer

    def put(self, request, *args, **kwargs):
        response = check_box_threshold(request)
        if response is not None:
            return response

        request.POST._mutable = True
        user_id = request.user.id
        length = int(request.data['length'])
        width = int(request.data['width'])
        height = int(request.data['height'])
        area = 2 * (length * width + width * height + height * length)
        volume = length * width * height
        request.data['volume'] = volume
        request.data['area'] = area
        request.data['created_by'] = user_id
        request.data['updated_by'] = user_id

        return self.update(request, *args, **kwargs)


class BoxDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    queryset = Box.objects.all()
    serializer_class = BoxesSerializer


class ListUserBoxes(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    queryset = Box.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = BoxUserFilters

    serializer_class = BoxesSerializer

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        is_staff = request.user.is_staff
        user_id = request.user.id
        if is_staff:
            queryset = queryset.filter(created_by=user_id)
        else:
            return Response({
                "details": "Only Staff user can be able to see his/her created boxes in the store"

            }, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BaseManageView(APIView):
    """
    The base class for ManageViews
        A ManageView is a view which is used to dispatch the requests to the appropriate views
        This is done so that we can use one URL with different methods (GET, PUT, etc)
    """
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'VIEWS_BY_METHOD'):
            raise Exception('VIEWS_BY_METHOD static dictionary variable must be defined on a ManageView class!')
        if request.method in self.VIEWS_BY_METHOD:
            return self.VIEWS_BY_METHOD[request.method]()(request, *args, **kwargs)

        return Response(status=405)

class BoxUpdateDeleteManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        'DELETE': BoxDestroyView.as_view,
        'PUT': UpdateBoxView.as_view,
    }