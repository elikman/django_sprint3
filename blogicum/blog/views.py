from django.db.models.functions import Now
from django.shortcuts import get_object_or_404, render

from .models import Category, Post

PUBLISHED_POSTS = Post.objects.filter(
    is_published=True,
    category__is_published=True,
    pub_date__lte=Now()
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
