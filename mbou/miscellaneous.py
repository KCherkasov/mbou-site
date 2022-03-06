OBJS_PER_PAGE = 8

def paginate(objects, request, key='', opp=OBJS_PER_PAGE):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    key = key + '_page'

    PAGES_LEFT_RIGHT = 4

    page = request.GET.get(key)
    paginator = Paginator(objects, opp)

    try:
        result = paginator.page(page)
    except EmptyPage:
        result = paginator.page(1)
    except PageNotAnInteger:
        result = paginator.page(1)

    result.from_left = result.number - PAGES_LEFT_RIGHT
    result.from_right = result.number + PAGES_LEFT_RIGHT
    result.key = key

    return result
