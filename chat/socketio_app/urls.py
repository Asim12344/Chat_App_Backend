from django.urls import path
from .api import TempCreateView

urlpatterns = [
    path('temp', TempCreateView.as_view()),
]