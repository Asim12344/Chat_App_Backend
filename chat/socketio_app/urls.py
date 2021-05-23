from django.urls import path
from .views import TempCreateView

urlpatterns = [
    path('temp', TempCreateView.as_view()),
]