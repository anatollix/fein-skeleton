from django.contrib import admin

from blog.models import Post, PostAdmin, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    search_fields = ['name', 'slug', 'order']
    list_editable = ['order']
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
