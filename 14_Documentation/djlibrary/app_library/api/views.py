from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from app_library.models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from django_filters import rest_framework as filters


class BookFilter(filters.FilterSet):
    min_num_of_pages = filters.NumberFilter(field_name="num_of_pages", lookup_expr='gt')
    max_num_of_pages = filters.NumberFilter(field_name="num_of_pages", lookup_expr='lt')
    exact_num_of_pages = filters.NumberFilter(field_name="num_of_pages", lookup_expr='exact')

    class Meta:
    	model = Book
    	fields = [
    		'name',
    		'author', 
        	'min_num_of_pages', 
        	'exact_num_of_pages', 
        	'max_num_of_pages'
        	]


class AuthorViewSet(viewsets.ModelViewSet, generics.ListAPIView):
	queryset = Author.objects.all()
	serializer_class = AuthorSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['name']


class BookViewSet(viewsets.ModelViewSet, generics.ListAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_class = BookFilter