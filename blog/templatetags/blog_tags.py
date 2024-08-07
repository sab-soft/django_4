from django import template
from ..models import Post 

from django.db.models import Count

from django.utils.safestring import mark_safe
import markdown

# Each module that contains template tags need to define a variable called register 
# to be a valid tag library. This variable is an instance of template.library.
register = template.Library()

# Decorator added to the function, to register it as a simple tag.
@register.simple_tag

# We define a tag called total_posts as a Function to return the total number of 
# posts published.
# Django will use the function's name as the tag name. 
# Otherwise define a custome name as @register.simple_tag(name='my_tag')
def total_posts():
    return Post.published.count()

# Decorator : specified template to be rendered with the returned values.
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5): # option count parameter that defaults to 5.
    latest_posts = Post.published.order_by('-publish')[:count] # count limit the 
    # result of the the above query 
    
    # Returns a dictionary of variables instead of a simple value.
    # This is because, it is used as the context to render the specified template. 
    return {'latest_posts':latest_posts} 

# Most commented tag 
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments') # aggregate the total number of comments for each post.
    ).order_by('-total_comments')[:count] # order query result in descending order 
                                            # limit query result with optional parameter
# Markdown
# template filters are registered same as template tags 
# note function = markdown_format and filter=markdown
@register.filter(name='markdown')                                            
def markdown_formats(text):
    return mark_safe(markdown.markdown(text))