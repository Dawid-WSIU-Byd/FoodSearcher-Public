from django.db import models


# Create your models here.
class Ingredient(models.Model):
    IngredientName = models.CharField(max_length=100, default='N/A')  # Ingredient name, 100 is the safest option.
    IngredientId = models.PositiveIntegerField(unique=True)  # Spoonacular ID

    def __str__(self):
        return '[Ingredient: {}] = {}'.format(self.IngredientName, self.IngredientId)


class Recipe(models.Model):
    RecipeId = models.PositiveIntegerField(unique=True)
    Likes = models.PositiveIntegerField(default=0)
    # Sorry, can't store anything from API!

    def __str__(self):
        return '[ID: {}] = {} likes'.format(self.RecipeId, self.Likes)


class Comment(models.Model):
    CommentPost = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    Username = models.CharField(max_length=20)
    Mail = models.EmailField()
    Text = models.TextField(max_length=280)
    PostedOn = models.DateTimeField(auto_now_add=True)
    Active = models.BooleanField(default=False)

    class Meta:
        ordering = ['PostedOn']

    def __str__(self):
        return '{} says... {}'.format(self.Username, self.Text)


class Like(models.Model):
    LikePost = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='unq_likes')
    IP = models.GenericIPAddressField()
    IsLiked = models.BooleanField(default=True)

    class Meta:
        ordering = ['IP', 'IsLiked']

    def __str__(self):
        displayed = self.IsLiked and "+1" or "0"
        return '{} from {}'.format(displayed, self.IP)
