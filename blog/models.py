from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse 

from taggit.managers import TaggableManager

# Create a custome manager for all published post 
class PublishedManager(models.Manager):
    def get_queryset(self):
        # overidden the super (default) get_queryset function 
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    
# Create Post model 
class Post(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED ='PB', 'Published'
        
    title = models.CharField(max_length=250)
    # publish is an instance of datetime field but unique is set on date only
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, 
                              choices=Status.choices, 
                              default=Status.DRAFT)
    
    # User model from django.contrib.auth.models 
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_post')
    objects = models.Manager() # the default manager 
    published = PublishedManager() # our custom manager 
    # define a tag variable and assigned the TaggableManager() 
    tags = TaggableManager()
    
    
    # Meta class for sorting publish post 
    class Meta:
        ordering = ['-publish']
        
    # Meta class indexing the publish field 
        indexes = [
            models.Index(fields=['-publish']), 
        ]
    # Return human readable name for the model object 
    def __str__(self):  
        return self.title
    
    # Define a function to return absolute url of a post 
    # That most preferred url  to a post 
    # postitional arguments needed by the view is also passed 
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, 
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])
        
# Comment models
# A forign key is added to link every comment to a single post (many-to-one relationship)
# A related_name is defined to allow for naming attribute for relationship from the 
# related object back to this one i.e comments.post to retrieve the post of a comment or 
# post.comments.all() to retreive all comments associated with a post 
# default related objects is set by django as model name plus _set i.et comment_set to 
# name all related object of the object to the object of the model, where this 
# relationship is defined. 

class Comment(models.Model):
    post = models.ForeignKey(Post, 
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # BooleanField is set on this attribute to allow for manual activating or deactivating
    # a comment from the administration site. Default true means all are visible.
    active = models.BooleanField(default=True)
    
    
    class Meta:
        # Sort comments in chronologicall order by default 
        ordering = ['created']
        # This index will improve the performance of database lookups or ordering 
        # results using the created fields. 
        indexes = [models.Index(fields=['created'])]

        def __str__(self):
            return f'commet by {self.name} on {self.post}'
        
