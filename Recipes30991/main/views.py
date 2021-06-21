# Applications
from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path
import csv
import spoonacular
import json

# Django imports
from .models import Ingredient, Recipe, Comment, Like
from .forms import CommentForm

# Ingredients CSV, which is loaded at the start.
csvDirectory = Path(__file__).parents[1] / 'top-1k-ingredients.csv'

# API key storage. Use .gitignore to hide the 'secret' folder on GitHub. This practice should offer a lot of security.
# It's worth noting Spoonacular API uses points as calls. With free plan it's 150 points per day.
apiKey = ''
secretDirectory = Path(__file__).parents[1] / 'secret'
apiKeyDirectory = secretDirectory / 'auth.txt'
with open(apiKeyDirectory, 'r') as file:
    apiKey = file.read()
spoonAPI = spoonacular.API(apiKey)

# Development test
DEVTEST = True
devTestDirectory = Path(__file__).parents[1] / 'devtest'


# Gets all the ingredient entries from the CSV file. Those entries will be used for search.
# This function is used in the "getcsv" command.
# https://spoonacular.com/application/frontend/downloads/top-1k-ingredients.csv
def get_csv():
    checkIngredients = Ingredient.objects
    if checkIngredients:
        checkIngredients.all().delete()
    with open(csvDirectory, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            newIngredient = Ingredient()
            newIngredient.IngredientName = row[0]
            newIngredient.IngredientId = row[1] or 0
            newIngredient.save()


# A normal sort function which also creates a list for percentage ratio.
Percent = {}
def sort_percent_with_list(info):
    used = info['usedIngredientCount']
    missed = info['missedIngredientCount']
    percentage = used / (used + missed)
    Percent[info['id']] = "{:.2%}".format(percentage)
    return percentage


# Rendering the credits page.
def credits(request):
    data = {
        'Title': 'Credits',
    }
    return render(request, "main/credits.html", data)


# Rendering the about page.
def about(request):
    data = {
        'Title': 'About',
    }
    return render(request, "main/about.html", data)


# Rendering the recipe information page. It uses recipe's ID.
# Has a lot of logic - comments, likes, display...
def show_recipe(request, id):
    data = {
        'Title': 'No Name',
        'JSON_Instruction': None, 'JSON_Information': None,
        'CommentPost': None, 'Comments': None, 'NewComment': None, 'CForm': None,
        'IP': '0.0.0.0', 'Liked': False, 'Likes': 0,
    }
    if id:
        # IP
        try:
            data['IP'] = request.META['HTTP_X_FORWARDED_FOR']
        except:
            data['IP'] = request.META['REMOTE_ADDR']
        # API stuff
        if not DEVTEST:
            # GET: https://spoonacular.com/food-api/docs#Get-Recipe-Information
            # id, includeNutrition (1.1 points)
            response1 = spoonAPI.get_recipe_information(id, True)
            data['JSON_Information'] = response1.json()
            if response1:
                data['Title'] = data['JSON_Information']['title']
                # GET: https://spoonacular.com/food-api/docs#Get-Analyzed-Recipe-Instructions
                # id, stepBreakdown (1 point)
                response2 = spoonAPI.get_analyzed_recipe_instructions(id, True)
                data['JSON_Instruction'] = response2.json()
        else:
            with open(devTestDirectory / 'instruction.json', 'r') as file:
                data['JSON_Instruction'] = json.load(file)
            with open(devTestDirectory / 'information.json', 'r') as file:
                data['JSON_Information'] = json.load(file)
        # Recipe entry
        try:
            recipeById = Recipe.objects.get(RecipeId=id)
        except Recipe.DoesNotExist:
            recipeById = Recipe()
            recipeById.RecipeId = id
            recipeById.save()
        data['CommentPost'] = recipeById
        # Likes, check if like exists
        myLike = None
        if data['CommentPost'].unq_likes.filter(IP=data['IP']).exists():
            myLike = data['CommentPost'].unq_likes.get(IP=data['IP'])
            data['Liked'] = myLike.IsLiked
        data['Comments'] = data['CommentPost'].comments.filter(Active=True).order_by('-PostedOn', 'Username')
        if request.method == "POST":
            # Submitting a Comment
            data['CForm'] = CommentForm(data=request.POST)
            if data['CForm'].is_valid():
                newComment = data['CForm'].save(commit=False)
                newComment.CommentPost = data['CommentPost']
                newComment.save()
                data['NewComment'] = newComment
        else:
            data['CForm'] = CommentForm()
            # Submitting a Like
            if request.method == "GET":
                isFalse = request.GET.get('like') == "false"
                isTrue = request.GET.get('like') == "true"
                if isTrue or isFalse:
                    UpdateLike = False
                    if not myLike and isTrue: # Always give it a like, no matter what.
                        myLike = Like()
                        myLike.LikePost = data['CommentPost']
                        myLike.IP = data['IP']
                        UpdateLike = True
                    elif myLike and myLike.IsLiked != isTrue:  # We don't want to double-like
                        UpdateLike = True
                    if myLike and UpdateLike:
                        data['Liked'] = isTrue
                        myLike.IsLiked = isTrue
                        data['CommentPost'].Likes += (isTrue and 1 or -1)
                        myLike.save()
                        data['CommentPost'].save()
        # We're updating like status at the end
        data['Likes'] = data['CommentPost'].Likes
    # Render
    return render(request, "main/show_recipe.html", data)


# Rendering the possible recipes page. Recipes should be opened in a new tab.
def recipes(request):
    data = {
        'Title': 'Recipe Search',
        'JSON': None,
        'Ingredients': None, 'Percent': None, 'RecipeAmount': 0,
    }
    if request.method == "POST":
        data['Ingredients'] = request.POST.getlist('ingredientCheckbox')
        if not DEVTEST:
            # We're turning that array into a string.
            ingString = ','.join(str(e) for e in data['Ingredients'])
            # GET: https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients
            # ingredients, fillIngredients, limitLicense, number, ranking (1-2 points)
            response = spoonAPI.search_recipes_by_ingredients(ingString, None, None, 100, 1)
            data['JSON'] = response.json()
        else:
            with open(devTestDirectory / 'recipes.json', 'r') as file:
                data['JSON'] = json.load(file)
        # Get percentage for all the recipes and also sort the list by said percentage.
        Percent.clear()
        data['JSON'].sort(key=sort_percent_with_list, reverse=True)
        data['Percent'] = Percent.copy()
        data['RecipeAmount'] = len(data['Percent'])
    return render(request, "main/recipes.html", data)


# Rendering the starting page
def index(request):
    data = {
        'IngredientList': Ingredient.objects.all(),
    }
    return render(request, "main/index.html", data)
