from django.contrib import admin
from .models import Post, Comment, Category
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'text', 'created_at', 'img', 'category')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)