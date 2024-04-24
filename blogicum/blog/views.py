from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

BASE_POST_FILTER = Q(is_published=True) & Q(category__is_published=True)
LATEST_POST_COUNT = 5


def index(request):
    post_list = Post.objects.filter(
        BASE_POST_FILTER,
        pub_date__lte=timezone.now(),
    ).select_related('category', 'location')[:LATEST_POST_COUNT]
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, pk):
    post = get_object_or_404(
        Post.objects.filter(BASE_POST_FILTER),
        pk=pk,
        pub_date__lte=timezone.now(),
    )
    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug,
                                 is_published=True)
    post_list = Post.objects.filter(
        BASE_POST_FILTER,
        category=category,
        pub_date__lte=timezone.now(),
    ).select_related('category', 'location')
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context)
