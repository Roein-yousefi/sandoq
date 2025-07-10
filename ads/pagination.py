from rest_framework.pagination import PageNumberPagination
from django.conf import settings

class StandardResultsSetPagination(PageNumberPagination):
    page_size = getattr(settings , 'PAGINATION_PAGE_SIZE', 1)