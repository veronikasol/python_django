from rest_framework import serializers
from app_library.models import Author, Book

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Author
		fields = ['name', 'surname', 'year_of_birth']


class BookSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Book
		fields = ['name', 'isbn', 'year_of_publish', 'num_of_pages', 'author']