from django.contrib import admin

from .models import Post, Categories, Tags

# Register your models here.

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug','category', 'view', 'publish', 'status')
#     list_filter = ('status', 'created', 'publish', 'author')
#     search_fields = ('title', 'body')
#     prepopulated_fields = {'slug': ('title',)}
#     raw_id_fields = ('author',)
#     date_hierarchy = 'publish'
#     ordering = ('status', 'publish')
    


admin.site.register(Post)
admin.site.register(Categories)
admin.site.register(Tags)