from django.urls import path 
from . import views 

# Application namespace
app_name = 'blog'

urlpatterns = [
    # No argument, mapped to list_view 
    path('', views.list_view, name='post_list'), 
    # Mapped to post_detail and takes in one parameter id which 
    # matches an integer set by the path converter int.
    path('<int:id>/', views.post_detail, name='post_detail'),
]