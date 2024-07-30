from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse 

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
        return reverse('blog:post_detail', args=[self.id])