from django.contrib import admin
from .models import Category, Project
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name',


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'is_published', 'category', 'author',
    list_display_links = 'id', 'title'
    search_fields = 'id', 'title', 'author__username',
    list_filter = 'id', 'title', 'is_published', 'author__username',
    list_per_page = 10
    list_editable = 'is_published',
    prepopulated_fields = {
        "slug": ('title',)
    }
