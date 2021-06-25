from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination, CursorPagination

# the following below only works on viewset or generic view classes


class WatchListPagination(PageNumberPagination):
    page_size = 1
    # "http://localhost:8000/watch/list2/?p=2"
    page_query_param = 'p'  # load the 2nd page according to page_size

    # http://localhost:8000/watch/list2/?s=2"
    page_size_query_param = 's'  # only load 1st 2 records

    max_page_size = 1  # maximum elements on each page

    # last_page_strings default = 'last'
    # example: http://localhost:8000/watch/list2/?p=last

    last_page_strings = 'end'  # custom last page string


# LimitOffset= offset:50 means skip the 1st 50 items, and take the 51st according to limit
class WatchListLOPagination(LimitOffsetPagination):
    # "count": 4,
    # "next": "http://localhost:8000/watch/list2/?limit=1&offset=1",
    default_limit = 1
    max_limit = 10  # maximum allowable limit per request
    limit_query_param = 'limit'
    offset_query_param = 'start'  # custom value for default 'offset' parameter


# uses a cursor according to specific field from ordering parameter
# can't go on specific page unlike pagination
class WatchListCPagination(CursorPagination):
    page_size = 1
    ordering = 'created'
    cursor_query_param = 'record'  # changes default 'cursor' parameter
