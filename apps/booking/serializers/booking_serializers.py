from datetime import timedelta
from rest_framework import serializers
from apps.apartments.models.apartment_models import Apartment
from apps.apartments.serializers.apartment_serializers import ApartmentSerializer
from apps.booking.models.booking_models import Booking
from django.utils import timezone
from django.db.models import Q


class BookingSerializer(serializers.ModelSerializer):
    apartment = ApartmentSerializer()

    class Meta:
        model = Booking
        fields = ['renter', 'apartment', 'date_from', 'date_to', 'is_approved_by_landlord', 'is_canceled']
        read_only_fields = ['renter', 'is_canceled']


class AbstractBookingCreateDetailSerializer(serializers.ModelSerializer):
    def validate_apartment(self, value):
        if not Apartment.objects.filter(apartment_type=value, is_active=True).exists():
            raise serializers.ValidationError(
                'This apartment is disabled for reservations or does not exist'
            )
        return value

    def validate_date_from(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError(
                'Date From must be today or later'
            )
        return value

    def validate_date_to(self, value):
        if value < timezone.now().date() + timedelta(days=1):
            raise serializers.ValidationError(
                'Date To must be tomorrow or later'
            )
        return value


class BookingDetailsSerializer(AbstractBookingCreateDetailSerializer):
    class Meta:
        model = Booking
        fields = [
            'apartment',
            'date_from',
            'date_to',
            'is_approved_by_landlord',
            'is_canceled',
        ]

        read_only_fields = ['is_canceled','is_approved_by_landlord']

    def validate(self, data):
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        apartment = data.get('apartment')

        if date_from or date_to:
            if apartment is None:
                apartment = self.instance.apartment
            if date_from is None:
                date_from = self.instance.date_from
            if date_to is None:
                date_to = self.instance.date_to

            if date_from >= date_to:
                raise serializers.ValidationError(
                    'Date From must be earlier than Date To.'
                )

            check_dates_availability(apartment, date_from, date_to, self.instance.id)

        return data



class BookingCreateSerializer(serializers.ModelSerializer):
    apartment = serializers.PrimaryKeyRelatedField(
        queryset=Apartment.objects.filter(is_active=True),
        write_only=True
    )
    apartment_details = ApartmentSerializer(read_only=True, source='apartment')

    class Meta:
        model = Booking
        fields = [
            'renter',
            'apartment',
            'apartment_details',
            'date_from',
            'date_to',
            'is_approved_by_landlord',
            'is_canceled',
        ]
        read_only_fields = ['renter', 'is_approved_by_landlord', 'is_canceled']

    def validate(self, data):
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        apartment = data.get('apartment')

        if date_from >= date_to:
            raise serializers.ValidationError(
                'Date From must be earlier than Date To.'
            )

        check_dates_availability(apartment, date_from, date_to)

        return data


class CancelBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = [
            'renter',
            'apartment',
            'date_from',
            'date_to',
            'is_approved_by_landlord',
        ]

    def validate(self, data):
        is_canceled = data.get('is_canceled')
        date_from = self.instance.date_from
        if is_canceled and timezone.now().date() >= date_from - timedelta(days=3):
            raise serializers.ValidationError(
                "You can cancel your booking up to 3 days in advance."
            )
        return data


class ApproveBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['is_approved_by_landlord']
        read_only_fields = [
            'renter',
            'apartment',
            'date_from',
            'date_to',
            'is_canceled',
        ]


def check_dates_availability(apartment, date_from, date_to, booking_id=None):
    overlapping_reservations = Booking.objects.filter(
        apartment=apartment,
        is_canceled=False,
        is_approved_by_landlord=True,
        ).exclude(id=booking_id).filter(
        Q(date_from__lte=date_to) & Q(date_to__gte=date_from)
    )

    if overlapping_reservations.exists():
        raise serializers.ValidationError(
            'The apartment is already reserved for the selected dates.'
        )

