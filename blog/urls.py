from django.urls import path
from django.views.generic.base import TemplateView
from .views import HomePageView, RecipeView, AboutView, contactView, SubscriptionView, SubscriptionSuccessView, FoodCategoryView, AllCategoriesView

urlpatterns = [
    path ('', HomePageView.as_view(), name='homepage'),
    path ('about/', AboutView.as_view(), name='about'),
    path ('recipes/', AllCategoriesView.as_view(), name='recipes'),
    path ('contact/', contactView, name='contact'),
    path ('subscribe/', SubscriptionView.as_view(), name='subscribe'),
    path ('subscription-success/', SubscriptionSuccessView.as_view(), name='subscription_success'),
    path ('<category_url>/', FoodCategoryView.as_view(), name='food_category'),
    path ('<str:category>/<title_slug>/', RecipeView.as_view(), name='recipe'),
    path ("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]