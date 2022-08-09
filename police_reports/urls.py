from django.urls import path

from police_reports.views import CrimeViewSet

urlpatterns = [
    path('crime_reports/', CrimeViewSet.as_view({'get': 'list'}))
]
