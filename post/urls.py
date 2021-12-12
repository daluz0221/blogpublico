
from django.urls import path

from .views import PostListView, post_detail, post_share, PostCategoryListView, PostTagListView, contacto, PostKeyWordsListView

app_name = 'post'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('buscar-post/', PostKeyWordsListView.as_view(), name='post_list_palabra_clave'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('contacto/', contacto, name='contacto'),
    path('categorias/<categoria>/', PostCategoryListView.as_view(), name='post_category'),
    path('<tag>/', PostTagListView.as_view(), name='post_tag'),
]