from django.urls import path
from . import views

urlpatterns = [
    path('<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_type_pk>', views.blog_with_type, name='blogs_with_type'),
    path('', views.blog_list, name='blog_list'),
    path('date/<int:year>/<int:month>', views.blog_with_date, name='blog_with_date'),
]
