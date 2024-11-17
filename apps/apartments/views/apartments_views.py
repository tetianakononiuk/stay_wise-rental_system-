from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.apartments.filters.apartment_filters import ApartmentFilter
from apps.apartments.models.apartment_models import Apartment
from apps.apartments.serializers.apartment_serializers import ApartmentSerializer
from apps.users.permissions.landlord_permissions import IsLandlord, IsLandlordOwner


class ApartmentListCreateView(ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_set_class = ApartmentFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']
    serializer_class = ApartmentSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsLandlord]

        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_landlord:
            return Apartment.objects.all()
        else:
            return Apartment.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)


class ApartmentDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ApartmentSerializer
    queryset = Apartment.objects.all()

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsLandlordOwner]

        return [permission() for permission in self.permission_classes]

    def get_object(self):
        obj = get_object_or_404(Apartment, pk=self.kwargs['pk'])
        if not obj.is_active and not self.request.user.is_landlord:
            raise NotFound()
        self.check_object_permissions(self.request, obj)
        return obj
