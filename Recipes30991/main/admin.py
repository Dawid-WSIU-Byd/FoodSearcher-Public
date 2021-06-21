from django.contrib import admin
from .models import Ingredient, Recipe, Comment, Like


@admin.register(Ingredient)
class AdminDisplayIngredients(admin.ModelAdmin):
    search_fields = ('IngredientName', 'IngredientId')
    list_display = ('IngredientName', 'IngredientId')


@admin.register(Recipe)
class AdminDisplayRecipe(admin.ModelAdmin):
    search_fields = ('RecipeId', 'Likes')
    list_display = ('RecipeId', 'Likes')


@admin.register(Comment)
class AdminDisplayComments(admin.ModelAdmin):
    list_display = ('Username', 'Text', 'CommentPost', 'PostedOn', 'Active')
    list_filter = ('Active', 'PostedOn')
    search_fields = ('Username', 'Mail', 'Text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(Active=True)


@admin.register(Like)
class AdminDisplayLikes(admin.ModelAdmin):
    list_display = ('IP', 'IsLiked', 'LikePost')
    search_fields = ['IP']
