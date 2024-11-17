from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import SAFE_METHODS
from apps.booking.models.booking_models import Booking
from apps.booking.serializers.booking_serializers import BookingCreateSerializer, BookingSerializer, BookingDetailsSerializer, CancelBookingSerializer, ApproveBookingSerializer
from apps.users.permissions.landlord_permissions import IsLandlordOwnerOfReservationApartment, IsLandlord
from apps.users.permissions.renter_permissions import IsRenterOwner, IsRenter
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class BookingListCreateView(ListCreateAPIView):
    def get_serializer_class(self):

        if self.request.method == 'POST':
            return BookingCreateSerializer
        return BookingSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_landlord:
            return Booking.objects.filter(apartment__landlord=user).order_by('date_from')
        else:
            return Booking.objects.filter(renter=user).order_by('date_from')

    def get_permissions(self):

        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsRenter | IsLandlord]
        else:
            self.permission_classes = [IsRenter]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):

        serializer.save(renter=self.request.user)


class BookingDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookingDetailsSerializer

    def get_permissions(self):

        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsRenterOwner | IsLandlordOwnerOfReservationApartment]
        else:
            self.permission_classes = [IsRenterOwner]

        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        user = self.request.user

        if user.is_landlord:
            return Booking.objects.filter(apartment__landlord=user)
        return Booking.objects.filter(renter=user)

    def get_object(self):

        obj = get_object_or_404(Booking, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


class BookingCancelView(APIView):
    permission_classes = [IsRenterOwner]
    serializer_class = CancelBookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(renter=self.request.user)

    def get_object(self, pk):
        return Booking.objects.get(pk=pk)

    def post(self, request, pk):
        booking = self.get_object(pk)
        self.check_object_permissions(request, booking)

        serializer = CancelBookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingApproveView(UpdateAPIView):
    permission_classes = [IsLandlordOwnerOfReservationApartment]
    serializer_class = ApproveBookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(apartment__landlord=self.request.user, is_canceled=False)

    def get_object(self):
        obj = get_object_or_404(Booking, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):

        serializer.save(is_approved_by_landlord=True)