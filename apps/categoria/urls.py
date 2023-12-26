from django.urls import path
from .views import *


app_name="categoria"

urlpatterns = [


    path('all-articles/', AllArticlesView.as_view(), name="all_articles"),

    path('all-category/', AllCategoriaView.as_view(), name="all_category"),

    path('category/<int:category_id>/', AllCategoriaArticlesView.as_view(), name='all_category_articles'),

    path('create-category/', CategoryCreateView.as_view(), name="create_category"),

    path('<int:pk>/delete-category/', CategoryDeleteView.as_view(), name="delete_category")

]