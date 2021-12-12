from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Post, Categories, Tags
from .forms import EmailPostForm, EmailBlogForm
# Create your views here
# 
#.

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'post/list.html'

    
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        context['popular_post'] = Post.objects.all().order_by('-view')[:3]
        context['popular_tags'] = Tags.objects.all().order_by('-views')[:4]
        return context


class PostTagListView(ListView):
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'post/list.html'

   
    def get_queryset(self):
        tag = self.kwargs['tag']
       
        return Post.objects.filter(
            tags__name=tag
        ).order_by('publish')
    
    def get_context_data(self, **kwargs):
        context = super(PostTagListView, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        context['popular_post'] = Post.objects.all().order_by('-view')[:3]
        context['popular_tags'] = Tags.objects.all().order_by('-views')[:4]
        context['tag'] = self.kwargs['tag']
        return context
    


class PostKeyWordsListView(ListView):
    """Lista de Post por palabra clave"""
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'post/list2.html'

    
    def get_queryset(self):
        palabra_clave = self.request.GET.get("search", '')
        lista = Post.objects.filter(
            title__icontains=palabra_clave
        ).order_by('publish')
       
        return lista
    
    def get_context_data(self, **kwargs):
        context = super(PostKeyWordsListView, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        context['popular_post'] = Post.objects.all().order_by('-view')[:3]
        context['popular_tags'] = Tags.objects.all().order_by('-views')[:4]
        
        return context
    


class PostCategoryListView(ListView):
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'post/list.html'

    
    def get_queryset(self):
        categoria = self.kwargs['categoria']
        
        return Post.objects.filter(
            category__name=categoria
        ).order_by('publish')
    
    def get_context_data(self, **kwargs):
        context = super(PostCategoryListView, self).get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        context['popular_post'] = Post.objects.all().order_by('-view')[:3]
        context['popular_tags'] = Tags.objects.all().order_by('-views')[:4]
        context['categoria'] = self.kwargs['categoria']
        return context
    


def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post, slug=post, status='publicado', publish__year=year,publish__month=month, publish__day=day)
    categories = Categories.objects.all()
    post.view = post.view + 1
    for tag in post.tags.all():
    
        tag.views = tag.views + 1
        
        tag.save()
    post.save()
    popular_post = Post.objects.all().order_by('-view')[:3]
    popular_tags = Tags.objects.all().order_by('-views')[:4]

    return render(request, 'post/detail.html', {
        'post':post, 
        'categories': categories, 
        'popular_post': popular_post,
        'popular_tags': popular_tags
    })


def contacto(request):
    #Recupra el post por el id
    
    sent = False

    if request.method == 'POST':
        form = EmailBlogForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            #enviamos el correo
            
            subject = F"{cd['nombre']} {cd['apellido']} te escribió desde tu blog"
            message = F"comentarios de {cd['nombre']}: {cd['comentarios']}\n\nSu correo es: {cd['email']}"
            send_mail(subject, message, 'daluz0221@gmail.com', ['daluz0221@gmail.com'])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'post/contacto.html', {
         
        'form': form,
        'sent': sent
    })    


def post_share(request, post_id):
    #Recupra el post por el id
    post = get_object_or_404(Post, id=post_id, status='publicado')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #enviamos el correo
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = F"{cd['nombre']} {cd['apellido']} te recomendó leer {post.title}"
            message = F"Leer {post.title} en {post_url}\n\n comentarios de {cd['nombre']}: {cd['comentarios']}"
            send_mail(subject, message, 'daluz0221@gmail.com', [cd['para']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'post/share.html', {
        'post':post, 
        'form': form,
        'sent': sent
    })    
