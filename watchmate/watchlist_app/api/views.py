from django.shortcuts import get_object_or_404
from rest_framework import status, generics, viewsets, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.models import WatchList, StreamPlatform, Review

from .serializers import ReviewSerializer, StreamPlatformSerializer2, WatchListSerializer, StreamPlatformSerializer

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle

from django_filters.rest_framework import DjangoFilterBackend


class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle]

    # -----for filtering-------
    # def get_queryset(self):
    #     # self.kwargs['username'] is <string:username> from url
    #     # .../reviews/<username>/
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

    # -----for query parameter-----
    def get_queryset(self):
        # self.request.query_params.get('username', None) is from url
        # .../reviews/?username=<username>
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)


# --- concrete view classes ---
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    # override create method
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user  # access to logged in 'user' in request

        # check user if already reviewed this watchlist
        review_queryset = Review.objects.filter(
            watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")

        # todo: this calculation is wrong, should tally the existing average scores
        # then divide it with the review count

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (
                watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    # will use query parameter ../../?review_user__username=<username>&active=true
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    # override queryset
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    # the two below works together
    # add restriction according to this view
    # check settings.py to see the configuration
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'

# --- concrete view classes ---


# just like Viewset, but everything is inherited and automatically made
# ReadOnlyModelViewSet = no crud
# ModelViewSet = has crud
class StreamPlatformMVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


# ViewSet + Router = covers;
# /stream/<int:pk>
# /stream
class StreamPlatformVS(viewsets.ViewSet):
    permission_classes = [IsAdminOrReadOnly]

    def list(self, _):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, _, pk=None):
        queryset = StreamPlatform.objects.all()
        watchlist = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlatformSerializer(watchlist)
        return Response(serializer.data)

    def create(self, request):
        serializer = StreamPlatformSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# region "old code"
# class ReviewDetail(generics.GenericAPIView,
#                    mixins.RetrieveModelMixin):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# class ReviewList(generics.GenericAPIView,
#                  mixins.ListModelMixin,
#                  mixins.CreateModelMixin):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
# endregion

class StreamPlatformListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        platform = StreamPlatform.objects.all()
        # context={'request':request} argument is required for serializers.HyperlinkedRelatedField()
        # serializer = StreamPlatformSerializer(
        #    platform, many=True)

        # setup used for HyperlinkedModelSerializer
        serializer = StreamPlatformSerializer2(
            platform, many=True, context={'request': request}
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, _, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(
            instance=platform, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, _, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, _):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    # filtering (exact match)
    # watch/list2/?title=The Girl
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']

    # searching (with search options)
    # watch/list2/?search=the
    # search options:
    # ^ starts with
    # = exact match
    # @ full search (only for django postgresql backend)
    # $ regex search
    #
    #       example usage:
    #           search_fields = ['^title', '=platform__name']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'platform__name', 'avg_rating']

    # combine (reverse order for title using - prefix):
    # http://127.0.0.1:8000/watch/list2/?search=man&ordering=-title


class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, _, pk):
        try:
            movies = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movies)
        return Response(serializer.data)

    def put(self, request, pk):
        movies = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(instance=movies, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, _, pk):
        movies = WatchList.objects.get(pk=pk)
        movies.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
