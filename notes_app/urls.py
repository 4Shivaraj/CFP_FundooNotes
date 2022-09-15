from django.urls import path, include
from . import views

urlpatterns = [
    path('note/', views.NoteAV.as_view(), name='note'),
]
