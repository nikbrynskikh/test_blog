from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from django.utils import timezone
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

# Create your models here.



class Category(MPTTModel):
    """Модель категорий"""
    name = models.CharField(max_length=100, verbose_name='Имя')
    slug = models.SlugField(max_length=100, unique=True)
    parent = TreeForeignKey('self', verbose_name='Родительская категории', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = models.TextField("Описание", max_length=1000, default='', blank=True)
    template = models.CharField('Шаблон', max_length=500, default='blog/post_list.html')
    published = models.BooleanField('Отображать', default=True)
    paginated = models.PositiveIntegerField('Количество новостей на странице', default=5)
    sort = models.PositiveIntegerField('Порядок', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тэг')
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Post(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100, verbose_name='Название поста')
    mini_text = models.TextField()
    subtitle = models.CharField('Под-заголовок', max_length=500, blank=True, null=True)
    text = models.TextField()
    created_data = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, verbose_name='Тэг', blank=True)
    published_date = models.DateTimeField('Дата публикации', default=timezone.now, blank=True, null=True)
    edit_date = models.DateTimeField('Дата редактирования', default=timezone.now, blank=True, null=True)
    image = models.ImageField('Главная фотография', upload_to='post/', null=True, blank=True)
    template = models.CharField('Шаблон', max_length=500, default='new/post_detail.html')
    published = models.BooleanField('Опубликовать', default=True)
    viewed = models.PositiveIntegerField('Просмотрено', default=0)
    status = models.BooleanField('Для зарегистрированных', default=False)
    sort = models.PositiveIntegerField('Порядок', default=0)

    def __str__(self):
        return '{} {}'.format(self.title, self.mini_text)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        return reverse('detail_post', kwargs={'category': self.category.slug, 'slug': self.slug})

class Comment(models.Model):
    """Комментарий"""
    text = models.TextField()
    created_data = models.DateTimeField(auto_now_add=True)
    moderation = models.BooleanField(default=True)
    post = models.ForeignKey(Post, verbose_name='Статья', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.text, self.created_data)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

