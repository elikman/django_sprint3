from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

PUBLISHED_POSTS = Post.objects.filter(
    Q(is_published=True),
    Q(category__is_published=True),
    Q(pub_date__lte=timezone.now())
).select_related('category', 'location')

LATEST_POST_COUNT = 5


def index(request):
    post_list = PUBLISHED_POSTS[:LATEST_POST_COUNT]
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, pk):
    post = get_object_or_404(PUBLISHED_POSTS, pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    post_list = PUBLISHED_POSTS.filter(category=category)
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)
