from django.urls import path
import views

app_name = "main"

urlpatterns = [
    path(route="/", name="Index", view=views.Index),
]