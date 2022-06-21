from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.decorators import api_view
# Create your views here.

@api_view(["GET", "POST"])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializers = MovieSerializer(movies, many=True)
        return Response(serializers.data)
    
    if request.method == "POST":
        serializers = MovieSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)


@api_view(["GET", "PUT", "DELETE"])
def movie_details(request, pk):
    if request.method == "GET":
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        serializers = MovieSerializer(movie)
        return Response(serializers.data)
    
    if request.method == "PUT":
        movie = Movie.objects.get(pk=pk)
        serializers = MovieSerializer(movie, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)
        
    
    if request.method == "DELETE":
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        return Response({"message": "Movie deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    