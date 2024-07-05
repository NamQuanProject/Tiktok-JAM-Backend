from django.urls import path, include
from . import views


urlpatterns = [
    path("get-historyrec/", views.shopping_history_recommend),
    path("get-combinedrec/", views.combined_recommend)
]