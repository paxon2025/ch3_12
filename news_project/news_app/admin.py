from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date')
    list_filter = ('publication_date', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)

# Alternatively, without the decorator:
# admin.site.register(Post, PostAdmin)
