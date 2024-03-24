from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_posts(request, posts, per_page):
    paginator = Paginator(posts, per_page)
    page = request.GET.get('page')
    
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        paginated_posts = paginator.page(paginator.num_pages)

    return paginated_posts