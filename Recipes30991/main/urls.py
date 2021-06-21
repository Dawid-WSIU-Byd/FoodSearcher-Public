from django.urls import path
from . import views

urlpatterns = [
    # Functional
    path('', views.index, name='index'),
    path('recipes/', views.recipes, name='recipes'),
    path('recipes/<int:id>/', views.show_recipe, name='show_recipe'),
    # Informational
    path('about/', views.about, name='about'),
    path('credits/', views.credits, name='credits'),
]
