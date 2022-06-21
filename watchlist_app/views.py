from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.views import APIView
# Create your views here.


class MovieListView(APIView):

    def get(self, request):
        movies = Movie.objects.all()
        serializers = MovieSerializer(movies, many=True)
        return Response(serializers.data)
    
    def post(self, request):
        serializers = MovieSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)

        

class MovieDetailsView(APIView):
    
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        serializers = MovieSerializer(movie)
        return Response(serializers.data)

    def put(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        serializers = MovieSerializer(movie, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)
    
    def delete(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        return Response({"message": "Movie deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        
    