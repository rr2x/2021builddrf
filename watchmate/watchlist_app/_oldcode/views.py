# from .models import Movie
# from django.http import JsonResponse


# def movie_list(request):
#     # retrieve queryset (complex datatype)
#     movies_queryset = Movie.objects.all()

#     # dictionary -> list -> dictionary
#     data = {
#         'movies': list(movies_queryset.values())
#     }

#     # dictionary -> json
#     return JsonResponse(data)


# def move_detail(request, pk):
#     movie_queryset = Movie.objects.get(pk=pk)

#     data = {
#         'name': movie_queryset.name,
#         'description': movie_queryset.description,
#         'active': movie_queryset.active
#     }

#     return JsonResponse(data)
