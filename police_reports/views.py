from django.db.models import QuerySet
from rest_framework import viewsets, mixins

from police_reports.models import Crime
from police_reports.pagination import ResultSetPagination
from police_reports.serializers import CrimeSerializer


class CrimeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = CrimeSerializer
    pagination_class = ResultSetPagination
    ordering = ('crime_id',)

    def initial(self, request, *args, **kwargs):
        return super().initial(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Crime]:
        queryset = Crime.objects.all()

        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if date_from:
            queryset = queryset.filter(report_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(report_date__lte=date_to)

        return queryset
