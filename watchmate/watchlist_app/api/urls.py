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
    StreamPlatformMVS
)

router = DefaultRouter()
router.register('stream', StreamPlatformMVS, basename='streamplatform')


# each platform owns multiple watch lists
# each watch list owns multiple reviews

# base: .../watch/

# todo: rewrite serializers to only process/return less data

urlpatterns = [
    # all watchlist
    path('list', WatchListAV.as_view(), name='watch-list'),

    # specific watchlist
    path('<int:pk>', WatchDetailAV.as_view(), name='watch-detail'),

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


    path('stream/<int:pk>/review-create',
         ReviewCreate.as_view(), name='review-create'),

    # stream/platform - id of stream/platform - all reviews
    # get reviews for this stream/platform
    path('stream/<int:pk>/review', ReviewList.as_view(), name='review-list'),


    # stream/platform - review - id of review
    # get specific review
    path('stream/review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),


]
