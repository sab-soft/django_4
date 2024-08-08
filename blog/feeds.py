'''
A web feed is a data format (usually XML) that provides users with the most recently 
updated content. Users can subscribe to the feed using a feed aggregator, a software
that is used to read feeds and get new content notifications.
'''
import markdown 
from django.contrib.syndication.views import Feed 
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post 

# def a subclass of the Feed class of the syndication framework.
class LatestPostsFeed(Feed):
    # title, link and description attributes correspond to that of the RSS elements 
    # respectively. Reverse_lazy is used to generate the URL for the link attribute.
    # the reverse() method allows us to build URLS by their name and pass optional 
    # parameters. 
    title = 'My Music Blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'
    
    # this method retrieves the objects to be included in the feed. \
    # The last five published posts to be precised.
    # NOTE item; title, description, pubdate methods will receive each object 
    # returned by items() and return the title, description and publication
    # date for each item.
    def items(self):
        return Post.published.all()[:5]

    # this method retrieves the title of the object (post)
    def item_title(self, item):
        return item.title 
    
    # this method retrieves the description of the object (post body)
    # markdown is used to convert markdown content to HTML and the 
    # truncatewords_html() template filter to cut the description of posts 
    # after 30 words, avoidign unclosed HTML tags.
    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)
    
    # this method retrieves the publication date of the object (post publish)
    def item_pubdate(self, item):
        return item.publish
        