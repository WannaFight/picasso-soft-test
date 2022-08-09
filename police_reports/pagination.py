from rest_framework.pagination import PageNumberPagination


class ResultSetPagination(PageNumberPagination):
    page_size = 20
