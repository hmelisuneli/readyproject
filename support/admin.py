from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class SupportAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'time_create', 'time_update', 'get_html_photo', 'is_published',)
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content', 'id')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create', 'id')
    prepopulated_fields = {"slug": ("title",)}
    fields = (
        'title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Picture"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Support, SupportAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Support for students admin panel'
admin.site.site_header = 'Support for students admin panel'
