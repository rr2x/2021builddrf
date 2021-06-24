from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    WatchListAV,
    WatchDetailAV,
    StreamPlatformListAV,
    StreamPlatformDetailAV,
    ReviewCreate,
    ReviewList,
    ReviewDetail,
    StreamPlatformVS,
    StreamPlatformMVS,
    UserReview,
    WatchListGV
)

router = DefaultRouter()
router.register('stream', StreamPlatformMVS, basename='streamplatform')


# each platform owns multiple watch lists
# each watch list owns multiple reviews

# base: .../watch/

# todo: rewrite serializers to only process/return less data

urlpatterns = [
    # all watchlist
    path('list/', WatchListAV.as_view(), name='watch-list'),

    # specific watchlist
    path('<int:pk>/', WatchDetailAV.as_view(), name='watch-detail'),
    path('list2/', WatchListGV.as_view(), name='watch-detail'),

    # equivalent of:
    # /stream/<int:pk>
    # /stream/
    path('', include(router.urls)),

    # whole stream/platform
    # path('stream', StreamPlatformListAV.as_view(), name='stream-list'),

    # specific stream/platform
    # path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='stream-detail'),

    # path('review', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),


    path('<int:pk>/review-create/',
         ReviewCreate.as_view(), name='review-create'),

    # id of stream/platform - all reviews
    # get reviews for this stream/platform
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),


    # review - id of review
    # get specific review
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),


    path('reviews/', UserReview.as_view(), name='user-review-detail'),

    # for self.kwargs
    # path('reviews/<str:username>/', UserReview.as_view(),
    #      name='user-review-detail'),


]
