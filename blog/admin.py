from django.contrib import admin

from blog.models import Post, Category
from feincms.admin import item_editor


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    search_fields = ['name', 'slug', 'order']
    list_editable = ['order']
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)


class PostAdmin(item_editor.ItemEditor):
    date_hierarchy = 'published_on'
    list_display = ['title', 'status', 'last_changed', 'published_on', 'user', 'is_featured', 'tags']
    list_filter = ['status', 'published_on', 'is_featured']
    list_editable = ['is_featured', 'user', 'tags']
    search_fields = ['title', 'slug']
    prepopulated_fields = {
        'slug': ['title'],
        }
    fieldset_insertion_index = 1
    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'category', 'user', 'status', 'comment_status', 'is_featured'],
        }),
        ("Description", {
            'fields': ['excerpt', 'meta_description', 'meta_keywords', 'tags'],
        }),
        item_editor.FEINCMS_CONTENT_FIELDSET,
        ("Meta data", {
            'fields': ['published_on'],
        }),
    ]

    show_on_top = ['title', 'status', 'category', 'tags', 'user']
    raw_id_fields = ['user']

    @classmethod
    def add_extension_options(cls, *f):
        if isinstance(f[-1], dict):     # called with a fieldset
            cls.fieldsets.insert(cls.fieldset_insertion_index, f)
            f[1]['classes'] = list(f[1].get('classes', []))
            f[1]['classes'].append('collapse')
        else:   # assume called with "other" fields
            cls.fieldsets[0][1]['fields'].extend(f)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        obj.save()

admin.site.register(Post, PostAdmin)
