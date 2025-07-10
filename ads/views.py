from django.db.models.expressions import result

from .models import Ad
from .serializers import AdSerializer
from .pagination import StandardResultsSetPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from .permissions import IsPublisherOrReadOnly


class AdListApiView(APIView , StandardResultsSetPagination):
    serializer_class = AdSerializer

    def get(self,request):
        queryset = Ad.objects.filter(is_public=True)
        result = self.paginate_queryset(queryset , request)
        serializer = AdSerializer(instance=result, many=True)
        return self.get_paginated_response(serializer.data)



class AdCreateApiView(APIView):
    serializer_class = AdSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['publisher'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AdDetailApiView(APIView):
    serializer_class = AdSerializer
    def get(self,request,pk):
        queryset = Ad.objects.get(id=pk)
        serializer = AdSerializer(instance=queryset)
        return Response(serializer.data , status=status.HTTP_200_OK)


class AdUpdateApiView(APIView):
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated,IsPublisherOrReadOnly)
    parser_classes = (MultiPartParser,)

    def put(self,request,pk):
        queryset = Ad.objects.get(id=pk)
        serializer = AdSerializer(instance=queryset, data=request.data)
        if serializer.is_valid():
            serializer.validated_data['publisher'] = request.user
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdDeleteApiView(APIView):
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated,IsPublisherOrReadOnly)
    parser_classes = (MultiPartParser,)

    def delete(self,request,pk):
        queryset = Ad.objects.get(id=pk)
        queryset.delete()
        return Response({'response : Done'},status=status.HTTP_200_OK)

class AdSearchApiView(APIView , StandardResultsSetPagination):
    """ex : /api/ads/search/?q=benvis"""
    serializer_class = AdSerializer
    def get(self,request):
        q = request.GET.get('q')
        queryset = Ad.objects.filter(Q(title=q) | Q(caption=q))
        result = self.paginate_queryset(queryset, request)
        serializer = AdSerializer(result, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
