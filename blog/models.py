from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from django.db import models


class FoodCategory(models.Model):
    category = models.CharField(max_length=40)
    category_url = models.SlugField(max_length=60)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "food categories"

class BlogPost(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    food_category = models.ForeignKey('FoodCategory', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='content_images', blank=True)
    image_description = models.CharField(max_length=130)
    date = models.DateTimeField (auto_now_add=True)
    title = models.CharField(max_length=400)
    title_slug = models.SlugField(max_length=60)
    meta_description = models.CharField(max_length=160)
    keywords = models.CharField(max_length=200, blank=True, null=True)
    preview = models.CharField(max_length=180)
    calories = models.CharField(max_length=20, blank=True, null=True)
    preparation_time = models.CharField(max_length=20)
    cooking_time = models.CharField(max_length=20)
    total_time = models.CharField(max_length=20)
    final_quantity = models.CharField(max_length=40)
    text = models.TextField()

    def get_absolute_url (self):
        return reverse ('recipe', args=[str(self.title)])

    def __str__(self):
        return self.title
    

class RecipePart (models.Model):
    title = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title

class Ingredient (models.Model):
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    recipe_part = models.ForeignKey('RecipePart', blank=True, null=True, on_delete=models.CASCADE)
    ingredient = models.CharField (max_length=50)
    quantity = models.CharField(max_length=30, blank=True)
    unit = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.ingredient

class RecipeDirections (models.Model):
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    direction_name = models.CharField (max_length=250, blank=True)
    direction = models.TextField(blank=True)

    def __str__(self):
        return self.direction_name

class NutritionFact (models.Model):
    blog_post = models.OneToOneField('BlogPost', on_delete=models.CASCADE)
    serving_size = models.CharField(max_length=40, blank=True)
    calories = models.CharField(max_length=20, blank=True)
    calories_from_fat = models.CharField(max_length=20, blank=True)
    fat = models.IntegerField(help_text="g",blank=True, null=True)
    saturated_fat = models.IntegerField(help_text="g",blank=True, null=True)
    cholesterol = models.IntegerField(help_text="mg",blank=True, null=True)
    sodium = models.IntegerField(help_text="mg",blank=True, null=True)
    potassium = models.IntegerField(help_text="mg",blank=True, null=True)
    carbohydrates = models.IntegerField(help_text="g",blank=True, null=True)
    fiber = models.IntegerField(help_text="g",blank=True, null=True)
    sugar = models.IntegerField(help_text="g",blank=True, null=True)
    protein = models.IntegerField(help_text="g",blank=True, null=True)
    vitamin_A = models.IntegerField(help_text="mcg",blank=True, null=True)
    calcium = models.IntegerField(help_text="mg",blank=True, null=True)
    iron = models.IntegerField(help_text="mg",blank=True, null=True)

    def __str__(self):
        return self.blog_post.title

class AboutMe (models.Model):
    background_image = models.ImageField(upload_to='content_images', blank=True)
    profile_image = models.ImageField(upload_to='content_images', blank=True)
    image_description = models.CharField(max_length=130, blank=True, null=True)
    side_description = models.TextField(blank=True, null=True)
    full_description = models.TextField(blank=True, null=True)

    def __str__(self):
        self.name = 'Mateja'
        return self.name

class Subscription (models.Model):
    first_name = models.CharField (max_length=30)
    e_mail = models.EmailField (max_length=70)

    def __str__(self):
        return self.e_mail
