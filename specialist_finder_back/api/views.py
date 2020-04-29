import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from rest_framework import status, generics, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Category,Comment, Specialist
from .serializers import CategorySerializer, SpecialistSerializer, CommentSerializer, MyUserSerializer


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = MyUserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)

    return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(instance=category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(serializer.instance, request.data)
            return Response(serializer.data)
        return Response({'error': serializer.errors})
    elif request.method == 'DELETE':
        category.delete()
        return Response({'deleted': True})


class SpecialistListAPIView(APIView):
    def get(self, request):
        specialists = Specialist.objects.all()
        serializer = SpecialistSerializer(specialists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SpecialistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SpecialistDetailAPIView(APIView):
    def get_object(self, specialist_id):
        try:
            return Specialist.objects.get(id=specialist_id)
        except Specialist.DoesNotExist as e:
            return Response({'error': str(e)})

    def get(self, request, specialist_id):
        specialist = get_object_or_404(Specialist, pk=specialist_id)
        serializer = SpecialistSerializer(specialist)
        return Response(serializer.data)

    def put(self, request, specialist_id):
        specialist = get_object_or_404(Specialist, pk=specialist_id)
        serializer = SpecialistSerializer(instance=specialist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'errors': serializer.errors})

    def delete(self, request, specialist_id):
        specialist = get_object_or_404(Specialist, pk=specialist_id)
        Specialist.delete()

        return Response({'deleted': True})


class SpecialistByCategoryAPIView(APIView):
    def get(self, request, category_id):
        specialists = Specialist.objects.filter(category=category_id)
        serializer = SpecialistSerializer(specialists, many=True)
        return Response(serializer.data)


class TopTenSpecialistsAPIView(APIView):
    def get(self, request):
        top_ten = Specialist.objects.order_by('likes')[:10]
        serializer = SpecialistSerializer(top_ten, many=True)
        return Response(serializer.data)


class CommentsBySpecialistAPIView(generics.ListAPIView):
    def get_queryset(self):
        return Comment.objects.filter(specialist=self.kwargs.get('pk'))

    serializer_class = CommentSerializer


class FollowSpecialistAPIView(APIView):
    def put(self, request, specialist_id):
        specialist = Specialist.objects.get(id=specialist_id)
        if not request.user.is_authenticated:
            return Response({'message': 'Unauthorized user'}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        specialist.followers.add(user)
        user.specialistset.add(specialist)
        specialist.save()
        user.save()
        return Response({'message': 'User {} successfully followed specialist {}'.format(user.id, specialist_id)},
                        status=status.HTTP_200_OK)


class LikeSpecialistAPIView(APIView):
    def put(self, request, specialist_id):
        specialist = Specialist.objects.get(id=specialist_id)
        if not request.user.is_authenticated:
            return Response({'message': 'Unauthorized user'}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        specialist.likes += 1
        specialist.save()
        return Response({'message': 'Specialist {} successfully liked'.format(specialist_id)})


class SpecialistSearchAPIView(generics.ListCreateAPIView):
    search_fields = ['title']
    filter_backends = (filters.SearchFilter,)
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer
