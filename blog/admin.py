from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import BlogPost, FoodCategory, RecipePart, Ingredient, NutritionFact, AboutMe, Subscription, RecipeDirections


class FoodCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"category_url": ("category",)}

class RecipePartAdmin(admin.ModelAdmin):
    pass

class SubscriptionAdmin(admin.ModelAdmin):
    pass

class IngredientsInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class RecipeDirectionsInline(admin.StackedInline):
    model=RecipeDirections
    extra = 1

class NutritionFactInline(admin.StackedInline):
    model = NutritionFact
    extra = 1

class BlogPostAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
    prepopulated_fields = {"title_slug": ("title",)}
    fieldsets = [
        (None, {'fields': ['author', 'food_category', 'title', 'title_slug', 'preview', 'meta_description', 'keywords']}),
        ('Post Image', {'fields': ['image', 'image_description', 'medium_image', 'small_image']}),
        ('Body of the post', {'fields': ['text']}),
        ('Recipe', {'fields': ['final_quantity','calories','preparation_time','cooking_time','total_time']}),
    ]
    inlines = [IngredientsInline, RecipeDirectionsInline, NutritionFactInline]

class AboutMeAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'


admin.site.register (BlogPost, BlogPostAdmin)
admin.site.register (FoodCategory, FoodCategoryAdmin)
admin.site.register (RecipePart, RecipePartAdmin)
admin.site.register (AboutMe, AboutMeAdmin)
admin.site.register (Subscription, SubscriptionAdmin)

