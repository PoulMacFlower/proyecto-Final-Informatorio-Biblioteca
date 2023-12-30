from django.urls import path
from .views import *


app_name="articulos"

urlpatterns = [

    path('create/', ArtCreateView.as_view(), name="article_create"),

    path('all-articles/', AllArticlesView.as_view(), name="all_articles"),

    path('Article/<int:post_id>/', ArtDetailView.as_view(), name="detail_article"),

    path('<int:pk>/update/', ArtUpdateView.as_view(), name="update_article"),

    path('<int:pk>/delete-article/', ArtDeleteView.as_view(), name="delete_article"),

]