from django.urls import path 
from . import views 

from .feeds import LatestPostsFeed


# Application namespace
app_name = 'blog'

urlpatterns = [
    # No argument, mapped to list_view 
    path('', views.list_view, name='post_list'), 
    # list_view is called with an optional parameter tag_slug 
    path('tag/<slug:tag_slug>/', views.list_view, name='post_list_by_tag'),
    # int path converter is used for the year, month, and day 
    # whereas the slug path convert is used for the post parameter
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', 
         views.post_detail, name='post_detail'),
    # 
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    #
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    # url to the RSS feed
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]