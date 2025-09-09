from django.contrib import admin
from .models import Movie, Genre, Review


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'director', 'release_year', 'average_rating')
    list_filter = ['genre', 'release_year', 'director']
    search_fields = ('title', 'director', 'description')
    filter_horizontal = ('genre',)
    date_hierarchy = 'release_year'
    ordering = ['-release_year', 'title']

    fieldsets = (
        (None, {
            'fields': ('title', 'director', 'release_year')
        }),
        ('Details', {
            'fields': ('description', 'genre', 'average_rating')
        }),
    )
    readonly_fields = ['average_rating']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'user', 'rating', 'created_at')
    list_filter = ['rating', 'created_at', 'movie']
    search_fields = (
        'movie__title',
        'user__username',
        'review',
    )
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    fieldsets = (
        (None, {
            'fields': ('movie', 'user', 'rating')
        }),
        ('Review Content', {
            'fields': ('review',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']
