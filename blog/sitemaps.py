from django.contrib.sitemaps import Sitemap
from .models import ContentPost
 
 
class PostSitemap(Sitemap):    
    changefreq = "weekly"
    priority = 0.9
 
    def items(self):
        return ContentPost.objects.all()
 
    def lastmod(self, obj):
        return obj.pub_date