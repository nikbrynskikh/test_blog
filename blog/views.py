from datetime import datetime

from django.shortcuts import render
from django.views.generic.base import View
from .models import Category, Post

# Create your views here.

class HomeView(View):
    """Домашняя страница"""
    def get(self, request):
        categories = Category.objects.all()
        posts = Post.objects.filter(published_date__lte=datetime.now(), published=True)
        return render(request, 'blog/post_list.html', {'categories': categories, 'posts': posts})

class CategoryView(View):
    """Вывод статей категории"""
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        return render(request, 'blog/category_detail.html', {'category': category})

class PostDetaillView(View):
    """Вывод полной статьи"""
    def get(self, request, category, slug):
        categories = Category.objects.all()
        post = Post.objects.get(slug=slug)
        return render(request, 'blog/post_detail.html', {'categories': categories, 'post': post})

