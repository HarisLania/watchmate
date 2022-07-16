from msilib.schema import ServiceInstall

from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from .models import Review, WatchList, StreamPlatform
from .serializers import ReviewSerializer, WatchListSerializer, StreamPlatformSerializer
from rest_framework.views import APIView
# from rest_framework import mixins
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import ReviewerOrReadOnly, IsAdminOrReadOnly
# Create your views here.


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watch = WatchList.objects.get(pk=pk)
        reviewer = self.request.user
        review = Review.objects.filter(watchlist=watch, reviewer=reviewer)
        if review.exists():
            raise ValidationError('Review already exists')
        
        if watch.total_ratings == 0:
            watch.avg_rating = serializer.validated_data['rating']
        else:
            watch.avg_rating = (watch.avg_rating + serializer.validated_data['rating']) / 2
        
        watch.total_ratings += 1
        watch.save()
        
        serializer.save(watchlist=watch, reviewer=reviewer)
        
        

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ReviewerOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class WatchListView(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        watchlists = WatchList.objects.all()
        serializers = WatchListSerializer(watchlists, many=True)
        return Response(serializers.data)
    
    def post(self, request):
        serializers = WatchListSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)

        

class WatchListDetailsView(APIView):
    
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            watchlist = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"error": "WatchList not found"}, status=status.HTTP_404_NOT_FOUND)
        serializers = WatchListSerializer(watchlist)
        return Response(serializers.data)

    def put(self, request, pk):
        watchlist = WatchList.objects.get(pk=pk)
        serializers = WatchListSerializer(watchlist, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)
    
    def delete(self, request, pk):
        watchlist = WatchList.objects.get(pk=pk)
        watchlist.delete()
        return Response({"message": "WatchList deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class StreamPlatformView(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
    