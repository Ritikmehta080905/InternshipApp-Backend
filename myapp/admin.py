from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_year', 'created_at')
    search_fields = ('title', 'author')
    list_filter = ('publish_year', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'author')
        }),
        ('Additional Information', {
            'fields': ('description', 'publish_year', 'cover_image'),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
    )