# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Other URLs
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('create/', views.CreateCategoryView.as_view(), name='create_category'),
]
