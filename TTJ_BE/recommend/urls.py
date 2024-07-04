from django.urls import path, include
import views

urlpatterns = [
    path("get-rec",  views.getRec)
]