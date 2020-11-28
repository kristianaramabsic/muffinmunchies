from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import BlogPost, FoodCategory, AboutMe, Subscription, NutritionFact,Ingredient,RecipePart, RecipeDirections
from .forms import SubscriptionForm, ContactForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Prefetch
import datetime

class HomePageView (ListView):
    model = BlogPost
    template_name = 'homepage.html'
    context_object_name = 'all_blog_posts'

    ordering = ['-date']

    def get_context_data(self, *args, **kwargs):
       ctx = super(HomePageView, self).get_context_data(*args, **kwargs)
        # retrieving the most recent post
       ctx['most_recent_post'] = BlogPost.objects.order_by('-date')[0]
       ctx['other_posts'] = BlogPost.objects.all().order_by('-date')[1:]
       ctx['food_categories'] = FoodCategory.objects.all()
       ctx['about_me'] = AboutMe.objects.all()
       return ctx

class RecipeView (DetailView):
    model = BlogPost
    template_name = 'recipe.html'
    slug_field = 'title_slug'
    slug_url_kwarg = 'title_slug'

    def get_context_data(self, *args, **kwargs):
       # showing other recipes
       ctx = super(RecipeView, self).get_context_data(*args, **kwargs)
       ctx['other_recipes'] = BlogPost.objects.all().exclude(title = self.get_object().title)[:6]
       ctx['ingredients'] = Ingredient.objects.all().filter(blog_post = self.get_object().pk)
       ctx['part_ingredients'] = Ingredient.objects.all().filter(recipe_part = self.get_object().pk)
       ctx['directions'] = RecipeDirections.objects.all().filter(blog_post = self.get_object().pk)
       if NutritionFact.objects.all().filter(blog_post = self.get_object().pk):
            if NutritionFact.objects.get(blog_post = self.get_object().pk).fat:
                ctx['daily_fat'] = (NutritionFact.objects.get(blog_post = self.get_object().pk).fat/78)*100
            if NutritionFact.objects.get(blog_post = self.get_object().pk).saturated_fat:
                ctx['daily_saturated_fat'] = (NutritionFact.objects.get(blog_post = self.get_object().pk).saturated_fat/20)*100
            if NutritionFact.objects.get(blog_post = self.get_object().pk).cholesterol:
                ctx['daily_cholesterol'] = (NutritionFact.objects.get(blog_post = self.get_object().pk).cholesterol/300)*100
            if NutritionFact.objects.get(blog_post = self.get_object().pk).sodium:
                ctx['daily_sodium'] = (NutritionFact.objects.get(blog_post = self.get_object().pk).sodium/2300)*100
            if NutritionFact.objects.get(blog_post = self.get_object().pk).carbohydrates:
                ctx['daily_carbohydrates'] = (NutritionFact.objects.get(blog_post = self.get_object().pk).carbohydrates/275)*100
            if NutritionFact.objects.get(blog_post = self.get_object().pk).vitamin_A:
                ctx['daily_vitamin_a'] = (NutritionFact.objects.get(blog_post = self.get_object().pk).vitamin_A/900)*100
            if NutritionFact.objects.get(blog_post = self.get_object().pk).calcium:
                ctx['daily_calcium'] = (NutritionFact.objects.get(blog_post = self.get_object().pk).calcium/1300)*100
            if NutritionFact.objects.get(blog_post = self.get_object().pk).iron:
                ctx['daily_iron'] = (NutritionFact.objects.get(blog_post = self.get_object().pk).iron/18)*100
            if NutritionFact.objects.get(blog_post = self.get_object().pk).fiber:
                ctx['daily_fiber'] = (NutritionFact.objects.get(blog_post = self.get_object().pk).fiber/28)*100
            if NutritionFact.objects.get(blog_post = self.get_object().pk).protein:
                ctx['daily_protein'] = (NutritionFact.objects.get(blog_post = self.get_object().pk).protein/50)*100
            if NutritionFact.objects.get(blog_post = self.get_object().pk).potassium:
                ctx['daily_potassium'] = (NutritionFact.objects.get(blog_post = self.get_object().pk).potassium/4700)*100
       return ctx

class AboutView (TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_me'] = AboutMe.objects.all()
        context['food_categories'] = FoodCategory.objects.all()
        return context

def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
        author = AboutMe.objects.all()[0]
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['Your_email']
            message = form.cleaned_data['message']
            try:
                send_mail(from_email + ' ' + subject, message, 'contact@labzlink.com', ['kristian.arambasic@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, 'Thank you for contacting me. I will reply to your inquiry shortly.')
            return redirect('contact')
    return render(request, "contact.html", {'form': form, 'author':author})

class SubscriptionView (CreateView):
    form_class = SubscriptionForm
    success_url = reverse_lazy('subscription_success')
    template_name = 'subscribe.html'



class SubscriptionSuccessView (TemplateView):
    template_name = 'subscription_success.html'

class FoodCategoryView (ListView):
    model = FoodCategory
    template_name = 'food_category.html'
    context_object_name = 'food_categories'
    slug_field = 'category_url'
    slug_url_kwarg = 'category_url'
    

    def get_context_data(self, **kwargs):
        context = super(FoodCategoryView, self).get_context_data(**kwargs)
        category = self.kwargs['category_url']
        category_id = FoodCategory.objects.filter(category_url = category)[0]
        context['food_category'] = BlogPost.objects.filter(food_category_id = category_id)
        context['current_category'] = FoodCategory.objects.filter(category_url = category)[0]
        return context

class AllCategoriesView (ListView):
    model = FoodCategory
    template_name = 'recipes_by_category.html'
    context_object_name = 'food_categories'    

    def get_context_data(self, **kwargs):
        context = super(AllCategoriesView, self).get_context_data(**kwargs)
        context['pancakes_posts'] = BlogPost.objects.filter(food_category_id = 1)[:3]
        context['pancakes'] = FoodCategory.objects.filter(id= 1)[0]
        context['muffins_posts'] = BlogPost.objects.filter(food_category_id = 2)[:3]
        context['muffins'] = FoodCategory.objects.filter(id= 2)[0]
        context['proba'] =  FoodCategory.objects.prefetch_related(Prefetch('blogpost_set',queryset=BlogPost.objects.filter(id__lte=8))).all()
        #context['posts_in_category'] = FoodCategory.objects.get(request.object.id).blogpost_set.all()
        return context