from django.urls import path, include
from . import views


urlpatterns = [
    path("get-AIrec/",  views.AI_recommend_products),
    path("get-checkboxrec/", views.checkbox_category_recommend),
    path("get-historyrec/", views.shopping_history_recommend)
]