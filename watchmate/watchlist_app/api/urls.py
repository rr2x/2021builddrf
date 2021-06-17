from django.urls import path
from .views import MovieListAV, MovieDetailAV
#from .views import movie_list, movie_detail

urlpatterns = [
    path('list/', MovieListAV.as_view(), name='movie-list'),
    path('<int:pk>', MovieDetailAV.as_view(), name='movie-detail')
]
