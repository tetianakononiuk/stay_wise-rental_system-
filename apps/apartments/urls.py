from django.urls import path
from apps.apartments.views.apartments_views import ApartmentListCreateView, ApartmentDetailUpdateDeleteView


urlpatterns = [
    path("", ApartmentListCreateView.as_view()),
    path("<int:pk>/", ApartmentDetailUpdateDeleteView.as_view()),
]
