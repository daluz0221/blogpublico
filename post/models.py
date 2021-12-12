from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

from .managers import Ppio

class PublishManager(models.Manager):
    def get_queryset(self):
        
        return super(PublishManager, self).get_queryset().filter(status='publicado')


class Categories(models.Model):
    name = models.CharField('Nombre de Categoría', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorias'


class Tags(models.Model):
    name = models.CharField('Nombre del Tag', max_length=50)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'



class Post(models.Model):
    
    STATUS_CHOICES = (
        ('borrado', 'Borrado'),
        ('publicado', 'Publicado')
    )

    category = models.ForeignKey(Categories,related_name='post_category', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags)

    title = models.CharField('Título', max_length=100)
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    image = models.ImageField(upload_to='post')
    view= models.IntegerField(default=0)
    publish = models.DateTimeField('Publicado',default=timezone.now)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='Actualizado')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='borrado')


    objects = models.Manager()
    published = PublishManager()
    ppio = Ppio()


    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])