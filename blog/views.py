from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.core.mail import send_mail
# Paginator class, EmptyPage for out of range and PageNotAnInteger for value not integers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.views.decorators.http import require_POST

from taggit.models import Tag

from django.db.models import Count


# List view for displaying all blog post
# list_view takes two parameter, request and an optional tag_slug 
# this parameter are passed through the url 
def list_view(request, tag_slug=None):
    post_list = Post.published.all()
    
    # filter post list by tags
    tag = None 
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    
    # Instantiate the Pagination class to return 3 post per page 
    paginator = Paginator(post_list, 3)
    # Retrieve the page GET HTTP parameter. This parameter contains the requested 
    # page number. If the page parameter is not in the GET parameters of the request,
    # use the default value 1 to load the frist page of results.
    page_number = request.GET.get('page', 1)
    # Obtain the objects for the desired page by calling the page() method of Paginator.
    # This method returns a page object that we store in the posts variable 
    
    # Add a try and except to handle out of range pages by delivering the last page 
    try:
        posts=paginator.page(page_number)
    
    # if page number is not an integer deliver the first page 
    except PageNotAnInteger:
        posts = paginator.page(1)
        
    # if page_number is out of range deliver last page of results 
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
            
    return render(request, 'blog/post/list.html', {'posts':posts, 'tag':tag})

# Detail view for displaying a single blog post 
def post_detail(request, year, month, day, post):
    ''' # try part get the post in the database with id of id 
    try:
        post = Post.published.get(id=id)
    # except raise a Http404 if the post does not exist in the database 
    except Post.DoesNotExist:
        raise Http404('No Post Found')'''
    
    post = get_object_or_404(Post, slug=post,
                             publish__year=year,
                             publish__month=month, 
                             publish__day=day, 
                             status=Post.Status.PUBLISHED)
    
    # List all active comments for this post 
    # the related name comments is used here to retrieve all comment for a post
    # using post.comments
    comments = post.comments.filter(active=True)
    
    # Form for users to fill 
    form = CommentForm()
    
    # List of similar posts
    # Retrieve a python list of IDs for the tags of the current post (Each tag has an ID). 
    # The values_list() QuerySet returns tuples with the values for the given 
    # fields. Flat=True is passed to get singles values such as [1, 2, 3,...] instead
    # of one-tules such as [(1,), (2,), (3,) ...]
    posts_tags_ids = post.tags.values_list('id', flat=True)
    # Get all posts containing any of this tags excluding the current post itself.
    similar_posts = Post.published.filter(tags__in=posts_tags_ids)\
                                    .exclude(id=post.id)
    # Use Count aggregation function to generate a calculated field - same_tags - that 
    # contains the number of tags shared with all the tags queried 
    # Order the result by the number of shared tags (descending order) and by publish
    # to dispaly recent posts first for the posts with the same number of shared tags.
    # Slice the result to retrieve only the first four posts. 
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                    .order_by('-same_tags', '-publish')[:4]

    
    return render(request, 'blog/post/detail.html', 
                  {'post':post, 'comments':comments, 'similar_posts':similar_posts})


def post_share(request, post_id):
    # Retreive post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    
    sent = False 

    if request.method == 'POST':
        # form was submitted 
        form = EmailPostForm(request.POST)
        
        if form.is_valid():
            # form fields passed validation 
            cd = form.cleaned_data
            # ... send email 
            # build_absolute_uri builds a complete url including HTTP schema and 
            # and hostname whereas the get_absolute_url build the absolute path 
            # of the post using its the get_absolute_url() method. 
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read" f"{post.title}" 
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s \
                        comments: {cd['comments']}"
            # The subject, message are created using the cleaned data of the validated 
            # form. The email is sent to the email containted in the to field of the form.
            send_mail(subject, message, cd['email'], [cd['to']])

            # The variable sent is set to True after the mail have been sent 
            # The variable is used in the template to display a success message 
            # When the form is successfully submitted.
            sent = True 
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})


# the post comment take a request and post_id parameters 
# Manages the post submission 
# submitted using HTTP post method 
# Require_post decorator provided by Django allows for only post request fo this view 
# Django will throw a Http 405(method not allowed) if you try to access this view 
# with any other method 
@require_POST
def post_comment(request, post_id):
    # retrieve a published post using its id 
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted 
    # instantiate the form using the submitted post data and 
    # validate it using the is_valid() method. If invalid the templates is rendered 
    # wit the validation errors 
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a comment form object without saving it to the database 
        comment = form.save(commit=False)
        # Assign the post to the comment 
        comment.post = post 
        # Save the comment to the database 
        comment.save()
    
    return render (request, 'blog/post/comment.html', 
                   {'post':post, 'form':form, 'comment':comment})
