# FoodSearcher                                                              

## Introduction

The following web application was made as a part of my engineer's thesis called "Web application project. Recipe finder based on the ingredients listed".
I haven't done much work with web applications at the time I have written this. 
I still consider it a great work, which will motivate me to make more projects.
On June 21st 2021, said thesis was defended and I have received a degree in computer science.

This version of "FoodSearcher" is the one that I have presented to lecturers.
As one of the plans, I have decided to make the source code public, so many other developers can improve it or use it as an inspiration.

---

## Requirements

You need to create a "secret" folder in the Recipes30991 directory, to make sure the application works properly.

1. Spoonacular API key
A file inside of this folder named "auth.txt" will be used to store the said key.
You can get your key at the [Spoonacular API Console](https://spoonacular.com/food-api/console).

2. Django SECRET_KEY
A file inside of this folder named "djangosecret.txt" will be used to store SECRET_KEY.
An example tool you can use to generate one is [Django Secret Key Generator](https://miniwebtool.com/django-secret-key-generator/)

It's also worth mentioning that the database included is empty. 
You might want to create a superuser for this application and see how the "getcsv" command works.

---

## Special thanks

 - [Spoonacular](https://spoonacular.com/food-api) - WebAPI
 - [SpoonacularAPI by John W. Miller](https://github.com/johnwmillr/SpoonacularAPI) - Spoonacular API wrapper
 - [Bootswatch](https://bootswatch.com/) - "Minty" theme
 - [FontAwesome](https://fontawesome.com/) - wonderful icons

---

## TODO

 - A better documentation inside of scripts I have worked on. Better explanation of functions.
 - Other quality of life improvements.
