from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import Http404
from .models import Post, Category


def index(request):
    """Главная страница / Лента записей"""
    posts = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).select_related('category').order_by('-pub_date')[:5]
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, id: int):
    """Отображение полного описания выбранной записи"""
    post = get_object_or_404(Post, id=id, is_published=True)
    if post.category is not None and not post.category.is_published:
        raise Http404("Post is not available")
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug: str):
    """Отображение публикаций категории"""
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now(),
    ).select_related('category').order_by('-pub_date')
    return render(request, 'blog/category.html', {'category': category, 'posts': posts})