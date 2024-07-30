from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Post 

# List view for displaying all blog post 
def list_view(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts':posts})

# Detail view for displaying a single blog post 
def post_detail(request, id):
    ''' # try part get the post in the database with id of id 
    try:
        post = Post.published.get(id=id)
    # except raise a Http404 if the post does not exist in the database 
    except Post.DoesNotExist:
        raise Http404('No Post Found')'''
    
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    

    return render(request, 'blog/post/detail.html', {'post':post})
