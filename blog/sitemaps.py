'''
A sitemap is an XML file that tells search engiens the pages of your website, their
relevance, and how frequently they are updated. Using a sitempa will make the site 
more visible in search engine rankings because it helps CRAWLERS to index your 
website's content.
'''
from django.contrib.sitemaps import Sitemap
from .models import Post

# Inheriting the Sitemap class of the sitemap module 
class PostSitemap(Sitemap):
    # changefreq and priority indicate the change frequency of the post pages and 
    # their relevance in the website (NOTE: the maximum value is 1). 
    # NOTE both can be attributes or methods 
    changefreq = 'weekly'
    priority = 0.9
    
    # This method returns the QuerySet of objects to include in the sitemap. 
    # By default, Django calls the get_absolute_url() method on each object to retrive
    # its URL. NOTE to specify the URL for each object, add a location method to 
    # the sitemap class 
    def items(self):
        return Post.published.all()
    
    # This method recieves each object returned by items() and returns the last time
    # the object was modified
    def lastmod(self, obj):
        return obj.updated