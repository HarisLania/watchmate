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
from .permissions import ReviewerOrReadOnly
# Create your views here.


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watch = WatchList.objects.get(pk=pk)
        reviewer = self.request.user
        review = Review.objects.filter(watchlist=watch, reviewer=reviewer)
        if review.exists():
            raise ValidationError('Review already exists')
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

# class ReviewDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
    
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
class WatchListView(APIView):

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
    

      

# class StreamPlatformView(APIView):

#     def get(self, request):
#         stream_platforms = StreamPlatform.objects.all()
#         serializers = StreamPlatformSerializer(stream_platforms, context={'request': request}, many=True)
#         return Response(serializers.data)
    
#     def post(self, request):
#         serializers = StreamPlatformSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data)
#         else:
#             return Response(serializers.errors)

        

# class StreamPlatformDetailsView(APIView):
    
#     def get(self, request, pk):
#         try:
#             stream_platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({"error": "Stream Platform not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializers = StreamPlatformSerializer(stream_platform)
#         return Response(serializers.data)

#     def put(self, request, pk):
#         stream_platform = StreamPlatform.objects.get(pk=pk)
#         serializers = StreamPlatformSerializer(stream_platform, request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data)
#         else:
#             return Response(serializers.errors)
    
#     def delete(self, request, pk):
#         stream_platform = StreamPlatform.objects.get(pk=pk)
#         stream_platform.delete()
#         return Response({"message": "Stream Platform deleted successfully"}, status=status.HTTP_204_NO_CONTENT)