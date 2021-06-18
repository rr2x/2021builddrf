from django.urls import path
from .views import (
    WatchListAV,
    WatchDetailAV,
    StreamPlatformListAV,
    StreamPlatformDetailAV,
    ReviewList,
    ReviewDetail
)

urlpatterns = [
    path('list', WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>', WatchDetailAV.as_view(), name='watch-detail'),
    path('stream', StreamPlatformListAV.as_view(), name='stream-list'),
    path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='stream-detail'),
    path('review', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
]
